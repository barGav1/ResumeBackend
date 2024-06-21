import React, { useState } from 'react';
import '../styles/Home.css';
import resumeIcon from '../Files/Resume_icon.png';
import googleIcon from '../Files/Google.webp';
import linkedinIcon from '../Files/Linkedin.webp';
import api from '../api';

const Register = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: ''
    });
    const [error, setError] = useState('');

    const registerUser = async (user) => {
        try {
            const response = await api.post('/users/', user);
            console.log('User registered:', response.data);
            // Redirect to login page with registered query parameter
            window.location.href = './login?registered=true';
        } catch (error) {
            console.error('Error registering user:', error);
            if (error.response && error.response.status === 409) {
                // User already exists, handle accordingly (e.g., show error message)
                setError('User already exists please select a different username.');
                // You can display an error message to the user here
            } else {
                // Other registration errors, handle accordingly
                setError('Other registration error');
                // You can display a generic error message to the user here
            }
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const user = {
            email: formData.email,
            password: formData.password
        };
        await registerUser(user);
    };

    return (
        <div>
            <section className="bg-gray-50 dark:bg-gray-900">
                <div className="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
                    <a href="/#" className="flex items-center mb-6 text-2xl font-semibold text-gray-900 dark:text-white">
                        <img className="h-16 w-auto" src={resumeIcon} alt="Resume Icon" />
                    </a>
                    <div className="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700">
                        <div className="p-6 space-y-4 md:space-y-6 sm:p-8">
                            <div className="flex justify-center text-center">
                                <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
                                    Create Your Account Today!
                                </h1>
                            </div>
                            <div className="flex justify-center text-center">
                                <p>Your first step towards <br /> creating the perfect resume!</p>
                            </div>
                            {error && <p className='text-red-600'>{error}</p>}
                            <form className="space-y-4 md:space-y-6" onSubmit={handleSubmit}>
                                <div>
                                    <label htmlFor="email" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Your email</label>
                                    <input type="email" name="email" id="email" className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="name@company.com" required value={formData.email} onChange={handleChange} />
                                </div>
                                <div>
                                    <label htmlFor="password" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Password</label>
                                    <input type="password" name="password" id="password" placeholder="••••••••" className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required value={formData.password} onChange={handleChange} />
                                </div>
                                <div className="flex items-center justify-between">
                                    <div className="flex items-start"></div>
                                </div>
                                <button type="submit" className="w-full px-4 py-2 rounded-md bg-blue-500 text-white font-bold hover:bg-blue-700">Register now!</button>
                                <div className="flex justify-center">
                                    <p>Or continue with</p>
                                </div>
                                <div className="flex flex-row justify-center gap-10">
                                    <img className="h-16 w-auto" src={googleIcon} alt="Google Icon" />
                                    <img className="h-16 w-auto" src={linkedinIcon} alt="LinkedIn Icon" />
                                </div>
                                <p className="text-sm font-light text-gray-500 dark:text-gray-400">
                                    Already have an account? <a href="./Login" className="font-medium text-primary-600 hover:underline dark:text-primary-500">Login</a>
                                </p>
                            </form>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default Register;
