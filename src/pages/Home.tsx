import React from 'react';
import Layout from '@/components/layout/Layout';
import CatalogList from '@/components/parts/CatalogList';
import Pagination from '@/components/parts/Pagination';
import Info from '@/components/parts/Info';

const Home = () => {
    return (
        <Layout>
            <div
                className='
                    w-full flex flex-col min-h-[calc(100vh-70px)]
                '>
                <Info  />
                <CatalogList />
                <Pagination />
                <div
                    className='
                        h-[50px]
                        md:h-[75px]
                        lg:h-[100px]
                    '>
                </div>
            </div>
        </Layout>
    )
}

export default Home;