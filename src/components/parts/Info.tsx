import React from 'react';
import { CountrySelectors as Cs } from '@/redux/country';
import { useSelector } from 'react-redux';
import Vars from '@/constants/vars';

const showing = (page: number, pageCount: number) => {
    const showingCountries = pageCount - (page - 1) * Vars.Count.Post;

    return showingCountries > Vars.Count.Post ? Vars.Count.Post : showingCountries;
}

const Info = () => {
    const matchedCountries = useSelector(Cs.matched);
    const page = useSelector(Cs.page);
    const pageCount = useSelector(Cs.pageCount);
    const fetching = useSelector(Cs.fetching);

    return (
        <div
            className='
                w-full flex justify-center
            '>
            <div
                className='
                    w-full max-w-[85rem] flex justify-center pt-[10px] px-2.5
                    sm:px-5
                    md:px-10 md:pt-[15px]
                    lg:pt-[20px]
                '>
                {
                    fetching === false && pageCount > 0 &&
                        <div
                            className='
                                w-full max-w-[400px] flex flex-col gap-y-0.5
                                md:max-w-none md:gap-y-1
                                lg:gap-y-1.5
                            '>
                            <p
                                className='
                                    text-[13px] text-start text-[#505050]
                                    md:text-[14px]
                                    lg:text-[15px]
                                '>
                                Founded:&nbsp;
                                {matchedCountries.length}&nbsp;
                                {matchedCountries.length > 1 ? 'countries' : 'country'}
                            </p>
                            <p
                                className='
                                    text-[13px] text-start text-[#505050]
                                    md:text-[14px]
                                    lg:text-[15px]
                                '>
                                Showing:&nbsp;
                                {showing(page, matchedCountries.length)}&nbsp;
                                {showing(page, matchedCountries.length) > 1 ? 'countries' : 'country'}
                            </p>
                            <p
                                className='
                                    text-[13px] text-start text-[#505050]
                                    md:text-[14px]
                                    lg:text-[15px]
                                '>
                                Page: {page} / {pageCount}
                            </p>
                        </div>
                    
                }
            </div>
        </div>
    )
}

export default Info;