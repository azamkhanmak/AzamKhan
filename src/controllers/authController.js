const crypto = require('crypto');
const User = require('../models/User');

const hashPassword = (plainPassword) => {
  const salt = crypto.randomBytes(16).toString('hex');
  const hash = crypto
    .pbkdf2Sync(plainPassword, salt, 100000, 64, 'sha512')
    .toString('hex');

  return `${salt}:${hash}`;
};

const verifyPassword = (plainPassword, storedPassword) => {
  const [salt, originalHash] = storedPassword.split(':');

  if (!salt || !originalHash) {
    return false;
  }

  const hash = crypto
    .pbkdf2Sync(plainPassword, salt, 100000, 64, 'sha512')
    .toString('hex');

  return crypto.timingSafeEqual(
    Buffer.from(hash, 'hex'),
    Buffer.from(originalHash, 'hex')
  );
};

const registerUser = async (req, res) => {
  try {
    const {
      name,
      email,
      password,
      age,
      gender,
      religion,
      location,
      profession,
    } = req.body;

    if (
      !name ||
      !email ||
      !password ||
      age === undefined ||
      !gender ||
      !religion ||
      !location ||
      !profession
    ) {
      return res.status(400).json({
        message: 'All fields are required.',
      });
    }

    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(409).json({
        message: 'User with this email already exists.',
      });
    }

    const newUser = await User.create({
      name,
      email,
      password: hashPassword(password),
      age,
      gender,
      religion,
      location,
      profession,
    });

    return res.status(201).json({
      message: 'User registered successfully.',
      user: {
        id: newUser._id,
        name: newUser.name,
        email: newUser.email,
      },
    });
  } catch (error) {
    return res.status(500).json({
      message: 'Registration failed.',
      error: error.message,
    });
  }
};

const loginUser = async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({
        message: 'Email and password are required.',
      });
    }

    const user = await User.findOne({ email });
    if (!user) {
      return res.status(401).json({
        message: 'Invalid email or password.',
      });
    }

    const isPasswordValid = verifyPassword(password, user.password);
    if (!isPasswordValid) {
      return res.status(401).json({
        message: 'Invalid email or password.',
      });
    }

    return res.status(200).json({
      message: 'Login successful.',
      user: {
        id: user._id,
        name: user.name,
        email: user.email,
      },
    });
  } catch (error) {
    return res.status(500).json({
      message: 'Login failed.',
      error: error.message,
    });
  }
};

module.exports = {
  registerUser,
  loginUser,
};
