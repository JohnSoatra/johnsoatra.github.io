import React, { Fragment, useState } from 'react';
import { Dialog, Transition } from '@headlessui/react';
import { twMerge } from 'tailwind-merge';
import OtherInformation from './OtherInformation';
import Close from '@/assets/icons/close.png';

const Class = {
    'Title': `
        text-[14px] w-[120px] flex-shrink-0 text-[#505050]
        sm:w-[150px]
        md:text-[15px] md:w-[158px]
        lg:text-[16px] lg:w-[160px]
        xl:w-[200px]
    `,
    'Divider': `
        w-full h-px bg-[#eaeaea]
    `,
    'Value': `
        text-[14px] text-[#3366CC]
        md:text-[15px]
        lg:text-[16px]
    `,
    'Wrapper': `
        w-full flex items-start gap-x-1
    `,
    'PaddingX': `
        px-5
        md:px-5
        lg:px-8
    `
}

const Catalog = ({ country }: { country: any }) => {
    const [open, setOpen] = useState(false);

    return (
        <>
            <div
                className='
                    w-full flex flex-col items-center gap-y-4 py-3.5 bg-stone-50 border border-stone-300 rounded-[10px] shadow break-all
                    md:gap-y-5 md:py-4
                    lg:gap-y-6 lg:py-5
                '>
                <div
                    className={`
                        w-full flex flex-col gap-y-0.5 ${Class.PaddingX}
                        md:gap-y-1
                    `}>
                    <p
                        className={Class.Title}>
                        Flag:
                    </p>
                    <div
                        className='
                            w-full flex justify-center
                        '>
                        <div
                            className='
                                w-full aspect-video rounded-[5px] overflow-hidden border border-low
                            '>
                            <img
                                src={country.flags.png}
                                alt="flag"
                                className='h-full w-full'
                            />
                        </div>
                    </div>
                </div>
                <div
                    className='
                        w-full flex flex-col gap-y-[20px]
                        md:gap-y-[25px]
                        lg:gap-y-[30px]
                    '>
                    <div className={Class.Divider}></div>
                    <div
                        className={`
                            flex flex-col gap-y-0.5  ${Class.PaddingX}
                            md:gap-y-1
                            lg:gap-y-1.5
                        `}>
                        <p className={Class.Title}>
                            Official name:
                        </p>
                        <button
                            type='button'
                            className='
                                self-center text-center text-[20px] font-medium cursor-pointer transition-colors
                                md:text-[22px]
                                lg:text-[24px]

                                hover:text-black
                            '
                            onClick={() => setOpen(true)}>
                            {country.name.official}
                        </button>
                    </div>
                    <div className={Class.Divider}></div>
                </div>
                <div
                    className={`
                        w-full flex flex-col gap-y-2  ${Class.PaddingX}
                        md:gap-y-3
                        lg:gap-y-4
                    `}>
                    <div
                        className={
                            Class.Wrapper
                        }>
                        <p className={Class.Title}>
                            CCA2:
                        </p>
                        <p className={Class.Value}>
                            {country.cca2}
                        </p>
                    </div>
                    <div
                        className={
                            Class.Wrapper
                        }>
                        <p className={Class.Title}>
                            CCA3:
                        </p>
                        <p className={Class.Value}>
                            {country.cca3}
                        </p>
                    </div>
                    {
                        country.name.nativeName?.eng?.official !== undefined &&
                            <div
                                className={
                                    Class.Wrapper
                                }>
                                <p className={Class.Title}>
                                    Native name:
                                </p>
                                <p className={Class.Value}>
                                    {country.name.nativeName.eng.official}
                                </p>
                            </div>
                    }
                    <div
                        className="
                            w-full flex flex-col
                        ">
                        <p
                            className={
                                twMerge(
                                    Class.Title,
                                    `
                                        w-auto
                                        sm:whitespace-nowrap
                                        md:w-auto
                                        lg:w-auto
                                    `
                                )
                            }>
                            Alternative names:
                        </p>
                        <div
                            className={Class.Wrapper}>
                            <p className={Class.Title}></p>
                            <div
                                className='
                                    flex flex-col
                                '>
                                {
                                    country.altSpellings.map((alt: string, index: number) =>
                                        <p
                                            key={index}
                                            className={Class.Value}>
                                            {alt + ((index < country.altSpellings.length - 1) ? ',': '')}
                                        </p>
                                    )
                                }
                            </div>
                        </div>
                    </div>
                    <div
                        className={
                            Class.Wrapper
                        }>
                        <p className={Class.Title}>
                            IDD:
                        </p>
                        <p className={Class.Value}>
                            {country.idd.root}
                        </p>
                    </div>
                </div>
            </div>
            <Transition
                show={open}
                as={Fragment}>
                <Dialog
                    as="div"
                    className="
                        w-screen h-screen fixed top-0 left-0 flex justify-center items-center bg-black/20 backdrop-blur-sm z-20 px-2.5 py-5
                        md:py-10
                        lg:py-12
                    "
                    onClose={() => setOpen(false)}
                    onClick={() => setOpen(false)}>
                    <Transition.Child
                        as={Fragment}
                        enter="ease-out duration-300"
                        enterFrom="opacity-0 translate-y-5"
                        enterTo="opacity-100 translate-y-0"
                        leave="ease-in duration-100"
                        leaveFrom="opacity-100 translate-y-0"
                        leaveTo="opacity-0 translate-y-5">
                        <div
                            className='
                                w-full max-w-[500px] max-h-full relative py-3 px-5 pb-5 overflow-scroll rounded shadow-xl bg-white
                                md:max-w-[600px] md:px-10 md:py-5 md:pb-10
                                lg:px-12 lg:py-7 lg:pb-14
                            '
                            onClick={evt => evt.stopPropagation()}>
                            <div
                                className='
                                    sticky h-0 top-0 left-0 flex justify-end
                                '>
                                <button
                                    type='button'
                                    className='
                                        w-[14px] cursor-pointer opacity-40 transition
                                        md:w-[15px] md:h-6
                                        lg:w-[16px]
                                        hover:opacity-100
                                    '
                                    onClick={() => setOpen(false)}>
                                    <img
                                        src={Close}
                                        alt="close"
                                        sizes='100%'
                                    />
                                </button>
                            </div>
                            <div
                                className='
                                    flex flex-col gap-y-2
                                    md:gap-y-2.5
                                    lg:gap-y-3
                                '>
                                <h3
                                    className='
                                        text-[17px] top-0 left-0 pr-4
                                        md:text-[18px]
                                        lg:text-[19px]
                                    '>
                                    All information about <span className='font-medium'>{country.name.official}</span>.
                                </h3>
                                <OtherInformation
                                    country={country}
                                />
                            </div>
                        </div>
                    </Transition.Child>
                </Dialog>
            </Transition>
        </>
    )
}

export default Catalog;