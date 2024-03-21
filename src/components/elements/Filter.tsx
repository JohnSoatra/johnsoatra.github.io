import React, { Fragment, useEffect, useState } from 'react';
import Adjustment from '@/assets/icons/adjustment.png';
import { Dialog, Transition } from '@headlessui/react';
import { useDispatch, useSelector } from 'react-redux';
import { CountryActions as Ca, CountrySelectors as Cs } from '@/redux/country';
import { createSearchParams, useNavigate, useSearchParams } from 'react-router-dom';
import getKeyValues from '@/utils/search_params';

type RadioProps = {
    checked: boolean,
    radio: {
        value: string,
        label: string
    },
    onChange: (evt: React.ChangeEvent<HTMLInputElement>) => void,
}

const Radio = ({ checked, radio, onChange }: RadioProps) => {
    return (
        <div
            className='
                flex flex-row items-center
            '>
            <input
                type="radio"
                id={radio.value}
                name="sort"
                value={radio.value}
                checked={checked}
                className='
                    w-[15px] block 
                    lg:w-[16px]
                '
                style={{
                    accentColor: '#333'
                }}
                onChange={onChange}
            />
            <label
                htmlFor={radio.value}
                className='
                    px-2 text-[12px] block cursor-pointer transition-opacity select-none opacity-80
                    md:px-2.5 md:text-[13px]
                    lg:text-[14px]
                    hover:opacity-100
                '>
                {radio.label}
            </label>
        </div>
    );
}

const Radios: { value: string, label: string }[] = [
    {
        value: 'asc',
        label: 'A-Z'
    },
    {
        value: 'desc',
        label: 'Z-A'
    },
]

const Filter = () => {
    const dispatch = useDispatch();
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const [open, setOpen] = useState(false);
    const sortOrder = useSelector(Cs.sortOrder);
    const [currentSortOrder, setCurrentSortOrder] = useState(sortOrder);

    const changeRadio = (evt: React.ChangeEvent<HTMLInputElement>) => {
        if (evt.target.checked) {
            setCurrentSortOrder(evt.target.value);
        }
    }
    
    const saveClicked = async () => {
        dispatch(Ca.changeSortOrder(currentSortOrder));
        
        setTimeout(() => {
            if (window) {
                window.scrollTo({ top: 0 });
            }
        }, 50);

        navigate({
            pathname: '',
            search: createSearchParams({
                ...(await getKeyValues(searchParams)),
                page: '1',
                order: currentSortOrder
            }).toString()
        }, {replace: true});
    }

    useEffect(() => {
        if (open === true) {
            setCurrentSortOrder(sortOrder);
        }
    }, [open, sortOrder]);

    return (
        <>
            <button
                type='button'
                className='
                    w-[20px] cursor-pointer opacity-60 transition
                    md:w-[22px] md:h-6
                    lg:w-[24px]
                    hover:opacity-100
                '
                onClick={() => setOpen(true)}>
                <img
                    src={Adjustment}
                    alt="filter"
                    sizes='100%'
                />
            </button>
            <Transition
                show={open}
                as={Fragment}>
                <Dialog
                    as="div"
                    className="
                        w-screen h-screen fixed top-0 left-0  flex justify-center items-center bg-black/20 backdrop-blur-sm z-20 px-2.5
                    "
                    onClose={() => setOpen(false)}
                    onClick={() => setOpen(false)}>
                    <Transition.Child
                        as={Fragment}
                        enter="ease-out duration-150"
                        enterFrom="opacity-0 -translate-y-5"
                        enterTo="opacity-100 translate-y-0"
                        leave="ease-in duration-150"
                        leaveFrom="opacity-100 translate-y-0"
                        leaveTo="opacity-0 -translate-y-5">
                        <div
                            className='
                                w-full max-w-[300px] min-h-[300px] flex flex-col rounded shadow-xl bg-white py-2 px-3
                                md:max-w-[400px] md:px-5 md:py-3
                                lg:px-10 lg:py-4
                            '
                            onClick={(evt) => evt.stopPropagation()}>
                            <div
                                className='
                                    flex flex-col gap-y-1.5
                                    md:gap-y-2
                                '>
                                <p
                                    className='
                                        text-[13px]
                                        md:text-[14px]
                                        lg:text-[15px]
                                    '>
                                    Order by name:
                                </p>
                                <div
                                    className='
                                        flex flex-col gap-y-0.5
                                        md:gap-y-1
                                    '>
                                    {
                                        Radios.map((radio, index) =>
                                            <Radio
                                                key={index}
                                                radio={radio}
                                                checked={currentSortOrder === radio.value}
                                                onChange={changeRadio}
                                            />
                                        )
                                    }
                                </div>
                            </div>
                            <div className='flex-1'></div>
                            <div
                                className='
                                    w-full flex justify-end gap-x-2
                                '>
                                <button
                                    type="submit"
                                    className="
                                        text-[14px] transition  bg-white font-medium rounded-full px-4 py-2 text-center
                                        md:px-5 md:py-2.5
                                        hover:bg-gray-100
                                    "
                                    onClick={() => {
                                        setOpen(false);
                                    }}>
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    className="
                                        text-[14px] transition text-white border border-gray-600 bg-gray-600 font-medium rounded-full px-4 py-2 text-center
                                        md:px-5 md:py-2.5
                                        hover:bg-gray-700
                                    "
                                    onClick={() => {
                                        setOpen(false);
                                        saveClicked();
                                    }}>
                                    Save
                                </button>
                            </div>
                        </div>
                    </Transition.Child>
                </Dialog>
            </Transition>
        </>
    );
}

export default Filter;