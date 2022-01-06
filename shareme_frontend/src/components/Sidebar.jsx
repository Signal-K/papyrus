import React from 'react'
import { NavLink, Link } from 'react-router-dom';

// Assets & icons
import { RiHomeFill } from 'react-icons/ri';
import { IoIosArrowForward } from 'react-icons/io';
import logo from '../assets/logo.png';

// Style configuration/setup
const isNotActiveStyle = 'flex items-center px-5 gap-3 text-gray-500 hover:text-black transition-all duration-200 ease-in-out capitalize';
const isActiveStyle = 'flex items-center px-5 gap-3 font-extrabold border-r-2 border-black transition-all duration-200 ease-in-out capitalize';

// Categories mock data array (will be replaced with categories from Sanity)
const categories = [
    { name: 'Animals'},
    { name: 'Wallpapers'},
    { name: 'Photography'},
    { name: 'Gaming'},
    { name: 'Coding'},
    { name: 'Other'}
]

const Sidebar = ({ user, closeToggle }) => {
    const handleCloseSidebar = () => {
        if(closeToggle) closeToggle(false);
    }

    return (
        <div className="flex flex-col justify-between bg-white h-full overlow-y-scroll min-w-210 hide-scrollbar">
            <div className="flex flex-col">
                <Link
                    to="/"
                    className="flex px-5 gap-2 my-6 pt-1 w-190 items-center"
                    onClick={handleCloseSidebar}
                >
                    <img src={logo} alt="logo" className="w-full" />
                </Link>
                <div className="flex flex-col gap-5">
                    <NavLink
                        to="/"
                        className={({ isActive }) => isActive ? isActiveStyle : isNotActiveStyle}
                        onClick={handleCloseSidebar}
                    >
                        <RiHomeFill />
                        Home
                    </NavLink>
                    <h3 className="mt-2 px-5 text-base 2xl:text-xl">Discover Categories</h3>
                    {categories.slice(0, categories.length - 1).map((category) => ( // Do this for each category except the final one (which will be 'other')
                        <NavLink
                            to={`/category/${category.name}`}
                            className={({ isActive }) => isActive ? isActiveStyle : isNotActiveStyle}
                            onClick={handleCloseSidebar}
                            key={category.name}
                        >
                            {category.name}
                        </NavLink>
                    ))}
                </div>
            </div>
            { user && (
                // If user is logged in, show the user's profile and logout button (only show this content if user exists & is logged in)
                <Link
                    to={`user-profile/${user._id}`}
                    className="flex my-5 mb-3 gap-2 items-center bg-white rounded-lg shadow-lg mx-3"
                    onClick={handleCloseSidebar} // Close sidebar when user clicks on their profile/menu item
                >
                    <img src={user.image} className="w-10 h-10 rounded-full" alt="user-profile"/>
                    <p>{user.userName}</p>
                </Link>
            )}
        </div>
    )
}

export default Sidebar