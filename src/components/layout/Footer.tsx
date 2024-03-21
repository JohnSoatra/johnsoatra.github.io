import React from 'react';
import Github from '@/assets/icons/github.png';
import Linkedin from '@/assets/icons/linkedin.png';

const Contacts: { image: any, link: string }[] = [
    {
        image: Github,
        link: 'https://github.com/johnsoatra'
    },
    {
        image: Linkedin,
        link: 'https://www.linkedin.com/in/soatra'
    },
]

const Footer = () => {
    return (
        <div
            className='
                w-full flex justify-center z-10
            '>
            <div
                className='
                    w-full flex flex-col items-center
                '>
                <div
                    className='
                        w-full flex justify-center bg-gray-100/80 px-2.5 border-y border-gray-200
                        md:px-5
                        lg:px-10
                    '>
                    <div
                        className='
                            w-full max-w-[78rem] flex flex-col items-center gap-y-2 py-3 
                            md:py-6 md:gap-y-3
                            lg:py-9 lg:gap-y-4
                        '>
                        <p
                            className='
                                text-[18px] text-center
                                md:text-[20px]
                                lg:text-[22px]
                            '>
                            Powered by <span className='font-medium'>John Soatra</span>.
                        </p>
                        <div
                            className='
                                flex items-center gap-x-2
                                md:gap-x-3
                                lg:gap-x-4
                            '>
                            {
                                Contacts.map((contact, index) =>
                                    <a
                                        key={index}
                                        href={contact.link}
                                        rel='noreferrer'
                                        target='_blank'
                                        className='
                                            w-[20px] block opacity-70
                                            md:w-[25px]
                                            lg:w-[30px] hover:opacity-100
                                        '>
                                        <img
                                            src={contact.image}
                                            alt="contact"
                                            sizes='100%'
                                        />
                                    </a>
                                )
                            }
                        </div>
                    </div>
                </div>
                <p
                    className='
                        w-full text-center text-[12px] px-2.5 py-2.5
                        md:text[13px] md:px-5 md:py-3
                        lg:text-[14px] lg:px-10 lg:py-4
                    '>
                    Copyright © 2024. All right reserved.
                </p>
            </div>
        </div>
    );
}

export default Footer;