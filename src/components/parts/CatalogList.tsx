import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { CountrySelectors as Cs } from '@/redux/country';
import { CountryActions as Ca } from '@/redux/country';
import Vars from '@/constants/vars';
import Catalog from '@/components/elements/Catalog';
import Loading from '@/components/elements/Loading';
import { createSearchParams, useNavigate, useSearchParams } from 'react-router-dom';
import Fuse from 'fuse.js'
import { isNumber } from '@/utils/number';
import NoFounded from '../elements/NoFounded';
import getKeyValues from '@/utils/search_params';

const SortOrders = ['asc', 'desc'];

const CatalogList = () => {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const [countries, setCountries] = useState([] as any[]);
    const [previousSearched, setPreviousSearched] = useState(null as string|null);
    const dispatch = useDispatch();
    const fetching = useSelector(Cs.fetching);
    const page = useSelector(Cs.page);
    const pageCount = useSelector(Cs.pageCount);
    const search = useSelector(Cs.search);
    const sortOrder = useSelector(Cs.sortOrder);
    const matchedCountries = useSelector(Cs.matched);

    useEffect(() => {
        const abortController = new AbortController();

        if (sessionStorage.getItem('countries') === null) {
            const getData = async () => {
                dispatch(Ca.changeFetching(true));

                async function getData() {
                    try {
                        const response = await fetch(`https://restcountries.com/v3.1/all`, {
                            signal: abortController.signal
                        });
                        const countries = await response.json();
        
                        sessionStorage.setItem('countries', JSON.stringify(countries));
        
                        dispatch(Ca.changePageCount(Math.ceil(countries.length / Vars.Count.Post)));
                        dispatch(Ca.changeFetching(false));
                    } catch {
                        setTimeout(() => {
                            getData();
                        }, 500);
                    }
                }

                getData();
            };

            getData();
        } else {
            dispatch(Ca.changeFetching(false));
        }

        return () => {
            abortController.abort();
        }
    }, [dispatch]);

    useEffect(() => {
        (async () => {
            if (fetching === false) {
                const allCountries = JSON.parse(sessionStorage.getItem('countries') || '[]');
                let newMatchedCountries = [...matchedCountries];
                let pageCount = 0;

                if (search !== previousSearched) {
                    if (search !== '') {
                        const fuse = new Fuse<any>(allCountries, {
                            keys: ['name.official'],
                        });
                        newMatchedCountries = fuse.search(search).map((each) => each.item);
                    } else {
                        newMatchedCountries = allCountries;
                    }
                    setPreviousSearched(search);
                }

                if (sortOrder === 'asc') {
                    newMatchedCountries = newMatchedCountries.sort((a, b) => a.name.official > b.name.official ? 1 : -1);
                } else {
                    newMatchedCountries = newMatchedCountries.sort((a, b) => a.name.official < b.name.official ? 1 : -1);
                }

                if (JSON.stringify(newMatchedCountries) !== JSON.stringify(matchedCountries)) {
                    dispatch(Ca.changeMatched(newMatchedCountries));
                }

                if (newMatchedCountries.length > 0) {
                    pageCount = Math.ceil(newMatchedCountries.length / Vars.Count.Post);
                }
                
                dispatch(Ca.changePageCount(pageCount));

                if (page <= pageCount) {
                    const startIndex = (page - 1) * Vars.Count.Post;
                    setCountries(newMatchedCountries.slice(startIndex, startIndex + Vars.Count.Post));
                } else {
                    if (pageCount > 0) {
                        navigate({
                            pathname: '',
                            search: createSearchParams({
                                ...(await getKeyValues(searchParams)),
                                page: '1'
                            }).toString()
                        }, {replace: true});
                    }
                }

            }
        })();
    }, [dispatch, fetching, search, previousSearched, sortOrder, page, matchedCountries, navigate, searchParams]);

    useEffect(() => {
        (async () => {
            setTimeout(() => {
                if (window) {
                    window.scrollTo({top: 0});
                }
            }, 50);

            if (fetching === false) {
                dispatch(Ca.changeFetching(true));

                if (
                    searchParams.get('page') === null ||
                    (
                        isNumber(searchParams.get('page')!) &&
                        +searchParams.get('page')! > 0
                    )
                ) {
                    const sortOrder = searchParams.get('order') || '';
                    const currentPage = +((searchParams.get('page')) || 1);
                    const currentSearch = searchParams.get('search') || '';

                    dispatch(Ca.changeSortOrder(SortOrders.includes(sortOrder) ? sortOrder : 'asc'));
                    dispatch(Ca.changePage(currentPage > 0 ? currentPage : 1));
                    dispatch(Ca.changeSearch(currentSearch));
                } else {
                    dispatch(Ca.changeFetching(false));

                    navigate({
                        pathname: '',
                        search: createSearchParams({
                            ...(await getKeyValues(searchParams)),
                            page: '1'
                        }).toString()
                    }, {replace: true});
                }

                dispatch(Ca.changeFetching(false));
            }
        })();
    }, [fetching, dispatch, searchParams, navigate]);

    return (
        <div
            className='
                w-full flex-1 flex justify-center
            '>
            <div
                className='
                    w-full min-h-full relative flex justify-center max-w-[85rem] px-2.5 pt-1
                    sm:px-5
                    md:px-10 md:pt-2
                    lg:pt-2.5
                '>
                {
                    fetching ?
                        <Loading /> :
                        pageCount === 0 ?
                            <NoFounded /> :
                            <div
                                className='
                                    w-full max-w-[400px] grid grid-cols-1 gap-y-8
                                    md:max-w-none md:grid-cols-2 md:gap-x-8
                                    lg:grid-cols-3
                                '>
                                {
                                    countries.map((country, index) =>
                                        <Catalog
                                            key={index}
                                            country={country}
                                        />
                                    )
                                }
                            </div>
                }
            </div>
        </div>
    )
}

export default CatalogList;