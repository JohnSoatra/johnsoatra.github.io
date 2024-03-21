import React from 'react';
import { CountryActions, CountrySelectors } from '@/redux/country';
import { useDispatch, useSelector } from 'react-redux';
import { createSearchParams, useNavigate, useSearchParams } from 'react-router-dom';
import getKeyValues from '@/utils/search_params';

const textClass = `
    text-[14px] cursor-pointer transition-all select-none
    md:text-[16px]
    lg:text-[18px]
`;

const Class = {
    PageNumber: (selected: boolean) => `
        ${textClass} p-2 underline-offset-4
        ${
            selected ?
                `
                    text-black opacity-100 underline
                ` : 
                `
                    opacity-75 hover:underline
                `
        }
        hover:opacity-100
    `,
    Action: (enable: boolean) => `
        text-[14px] cursor-default select-none 
        md:text-[16px]
        lg:text-[18px]
        ${
            enable ?
            `
                opacity-95
                hover:opacity-100 hover:underline
            ` :
            `
                opacity-40
            `
        }
        
    `
}

const ThreeDots = () => {
    return (
        <p
            className={`
                text-[16px] cursor-default select-none font-bold opacity-70
                md:text-[18px]
                lg:text-[20px]
            `}>
            ···
        </p>
    );
}

const Border = () => {
    return (
        <div
            className='
                bg-gray-300 h-full w-px
            '>
        </div>
    );
}

const Pagination = () => {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const page = useSelector(CountrySelectors.page);
    const pageCount = useSelector(CountrySelectors.pageCount);
    const fetching = useSelector(CountrySelectors.fetching);

    const numberClicked = async (evt: React.MouseEvent, newPage: number) => {
        evt.preventDefault();

        if (newPage !== page) {
            dispatch(CountryActions.changePage(newPage));
            navigate({
                pathname: '',
                search: createSearchParams({
                    ...(await getKeyValues(searchParams)),
                    page: newPage.toString()
                }).toString()
            });
        }
    }

    const nextClicked = async (evt: React.MouseEvent) => {
        evt.preventDefault();

        if (page < pageCount) {
            const newPage = page + 1;
            dispatch(CountryActions.changePage(newPage));
            navigate({
                pathname: '',
                search: createSearchParams({
                    ...(await getKeyValues(searchParams)),
                    page: newPage.toString()
                }).toString()
            });
        }
    }

    const previousClicked = async (evt: React.MouseEvent) => {
        evt.preventDefault();

        if (page > 1) {
            const newPage = page - 1;
            dispatch(CountryActions.changePage(newPage));
            navigate({
                pathname: '',
                search: createSearchParams({
                    ...(await getKeyValues(searchParams)),
                    page: newPage.toString()
                }).toString()
            });
        }
    }

    return (
        <div
            className={`
                flex justify-center mt-6 px-3
                sm:px-5
                md:mt-10
                lg:mt-14
            `}>
            <div
                className={`
                    w-full max-w-[78rem] flex justify-center
                `}>
                {
                    (
                        fetching === false &&
                        page > 0 &&
                        pageCount > 0 &&
                        page <= pageCount
                    ) &&
                        <div
                            className='
                                flex items-center gap-x-2 border border-gray-300 px-2 rounded select-none
                                md:gap-x-3 md:px-3
                                lg:gap-x-4 lg:px-4
                            '>
                            <a
                                href={`?page=${page - 1}`}
                                rel='navigate'
                                className={Class.Action(page > 1)}
                                onClick={previousClicked}>
                                Previous
                            </a>
                            <div
                                className='
                                    w-full h-full flex items-center gap-x-1
                                    md:gap-x-1.5
                                    lg:gap-x-2
                                '>
                                <Border />
                                {
                                    page > 1 &&
                                    <>
                                        <a
                                            href={`?page=${0}`}
                                            rel='navigate'
                                            className={Class.PageNumber(page === 1)}
                                            onClick={(evt) => numberClicked(evt, 1)}>
                                            1
                                        </a>
                                        {
                                            page > 2 &&
                                            <ThreeDots />
                                        }
                                    </>
                                }
                                <a
                                    href={`?page=${page}`}
                                    rel='navigate'
                                    className={Class.PageNumber(true)}
                                    onClick={(evt) => numberClicked(evt, page)}>
                                    {page}
                                </a>
                                {
                                    (pageCount > 1 && page < pageCount) &&
                                    <>
                                        {
                                            page < pageCount - 1 &&
                                            <ThreeDots />
                                        }
                                        <a
                                            href={`?page=${pageCount}`}
                                            rel='navigate'
                                            className={Class.PageNumber(page === pageCount)}
                                            onClick={(evt) => numberClicked(evt, pageCount)}>
                                            {pageCount}
                                        </a>
                                    </>
                                }
                                <Border />
                            </div>
                            <a
                                href={`?page=${page + 1}`}
                                rel='navigate'
                                className={Class.Action(page < pageCount)}
                                onClick={nextClicked}>
                                Next
                            </a>
                        </div>
                }
            </div>
        </div>
    );
}

export default Pagination;