import React from 'react';

const Loading = () => {
    return (
        <div
            className='
                w-full h-full flex items-center justify-center
            '>
            <h3
                className='
                    text-[18px] animate-pulse
                    md:text-[23px]
                    lg:text-[28px]
                '>
                Loading...
            </h3>
        </div>
    )
}

export default Loading;