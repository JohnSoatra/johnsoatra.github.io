import React from 'react';
import Routes from '@/constants/routes';
import Search from '../elements/Search';
import { Link } from 'react-router-dom';
import Filter from '../elements/Filter';

const Header = () => {
    return (
        <div
            className='
                w-full flex justify-center fixed top-0 left-0 bg-gray-100/80 backdrop-blur-sm z-10
            '>
            <div
                className='
                    w-full relative max-w-[78rem] h-[70px] flex items-center gap-x-2.5 px-2.5 py-1.5
                    md:gap-x-5 md:py-2 md:px-5
                    lg:gap-x-10 lg:px-10
                '>
                <Link
                    to={Routes.Home}
                    rel='home'
                    className='
                        group flex items-center gap-x-2
                        md:gap-x-2.5
                        lg:gap-x-3
                    '>
                    <div
                        className='
                            w-[30px]
                            lg:w-[35px]
                        '>
                        <img
                            src="/logo512.png"
                            alt="logo"
                            sizes='100%'
                        />
                    </div>
                    <p
                        className='
                            text-[20px] font-medium
                            md:text-[22px]
                            lg:text-[24px]
                        '>
                        Country
                    </p>
                </Link>
                <div
                    className='
                        w-full max-w-[350px] flex-1 flex items-center gap-x-1
                        sm:max-w-[380px]
                        md:max-w-[400px] md:absolute md:top-1/2 md:left-1/2 md:-translate-x-1/2 md:-translate-y-1/2 md:gap-x-3
                        lg:max-w-[500px] lg:gap-x-4
                    '>
                    <div
                        className='
                           flex-1
                        '>
                        <Search />
                    </div>
                    <div>
                        <Filter />
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Header;