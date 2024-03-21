import React from 'react';
import Layout from '@/components/layout/Layout';

const FourOFour = () => {
    return (
        <Layout>
            <div
                className='
                    w-full h-[calc(100vh-70px)] flex justify-center items-center
                '>
                <h1
                    className='
                        text-[30px] font-medium
                        md:text-[35px]
                        lg:text-[40px]
                    '>
                    Page not found!
                </h1>
            </div>
        </Layout>
    )
}

export default FourOFour;