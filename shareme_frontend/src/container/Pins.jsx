import React, { useState } from 'react';
import { Routes, Route } from 'react-router-dom';

// Components
import { Navbar, Feed, PinDetail, CreatePin, Search } from '../components';

const Pins = ({ user }) => {
    const [searchTerm, setSearchTerm] = useState('')

    return (
        <div className="px-2 md:px-5">
            <div className="bg-gray-50">
                <Navbar searchTerm={searchTerm} setSearchTerm={setSearchTerm} />
            </div>
            <div className="h-full">
                <Routes>
                    <Route path="/" element={<Feed />} />
                    <Route path="/category/:categoryId" element={<Feed />} />
                    <Route path="/pin-detail/:pinId" element={<PinDetail user={user} />} />
                    <Route path="/" element={<Feed />} />
                    <Route path="/" element={<Feed />} />
                </Routes>
            </div>
        </div>
    )
}

export default Pins
