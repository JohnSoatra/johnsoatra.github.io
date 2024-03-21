import React, { useEffect, useState } from 'react';
import Find from '@/assets/icons/find.png';
import { createSearchParams, useNavigate, useSearchParams } from 'react-router-dom';
import getKeyValues from '@/utils/search_params';

const Search = () => {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const [searchPhrase, setSearchPhrase] = useState('');

    const gotoSearch = async (searchString: string) => {
        if (
            searchString !== searchParams.get('search') &&
            !(searchString === '' && searchParams.get('search') === null)
        ) {
            navigate({
                pathname: '',
                search: createSearchParams({
                    ...(await getKeyValues(searchParams)),
                    search: searchString,
                    page: '1',
                }).toString()
            })
        }
    }

    useEffect(() => {
        const currentSearch = searchParams.get('search') || '';
        setSearchPhrase(currentSearch);
    }, [searchParams]);

    return (
        <form className='relative w-full h-full'>
            <div className="relative w-full h-full rounded-full">
                <input
                    autoComplete='off'
                    type="text"
                    id="search-dropdown"
                    placeholder="Search..."
                    value={searchPhrase}
                    className="
                        w-full h-full block px-3 pr-[30px] py-2.5 text-sm transition rounded-xl border border-gray-400 bg-white/70
                        md:px-5 md:py-3 md:pr-[33px]
                        placeholder:text-[#444]
                        hover:bg-white/90
                        focus:bg-white focus:shadow-md
                    "
                    onChange={(evt) => setSearchPhrase(evt.target.value)}
                    onKeyDown={(evt) => {
                        if (evt.key === "Enter") {
                            evt.preventDefault();
                            gotoSearch(searchPhrase);
                        }
                    }}
                />
                <button
                    type='submit'
                    className="
                        w-[20px] h-full absolute top-1/2 right-2.5 -translate-y-1/2
                        md:w-[22px]
                        lg:w-[24px]
                    "
                    onClick={(evt) => {
                        evt.preventDefault();
                        gotoSearch(searchPhrase)
                    }}>
                    <img
                        src={Find}
                        alt="find"
                        sizes='100%'
                    />
                </button>
            </div>
        </form>
    );
}

export default Search;