import React from 'react';
import isArray from '@/utils/is_array';
import isObject from '@/utils/is_object';
import { isLink, capitalize } from '@/utils/string';
import isBoolean from '@/utils/boolean';
import { isImageUrl } from '@/utils/utils';

const Class = {
    'Title': `
        text-[14px] text-[#505050] font-semibold whitespace-nowrap
        md:text-[15px]
        lg:text-[16px]
    `,
    'Divider': `
        w-full h-px bg-[#eaeaea]
    `,
    'Value': `
        text-[14px] text-[#3366CC]
        md:text-[15px]
        lg:text-[16px]
    `,
    'ValueLink': `
        text-[14px] text-[#3366CC] underline-offset-2
        md:text-[15px]
        lg:text-[16px]
        hover:underline
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

const Icon = ({ link }: { link: string }) => {
    return (
        <div
            className='
                lg:w-[13px]
                md:w-[14px]
                w-[15px]
            '>
            <img
                src={link}
                alt="flag"
                sizes='100%'
            />
        </div>
    )
}

const MakeBlog = ({ field, value }: { field: any, value: any }) => {
    return (
        <div
            className={`
                w-full flex
                ${
                    isObject(value) ?
                    'flex-col' : 
                    'flex-row'
                }
                ${
                    isImageUrl(value.toString()) && 'items-center'
                }
            `}>
            <p
                className={Class.Title}>
                • {capitalize(field)}:
            </p>
            <div
                className={`
                    ${
                        isObject(value) ?
                        `
                            pl-3
                            md:pl-6
                            lg:pl:9
                        `:
                        `
                            pl-1.5
                            md:pl-2
                            lg:pl-2.5
                        `
                    }
                `}>
                {
                    isObject(value) ?
                        Object.keys(value).map((_key, index) =>
                            <div
                                key={index}
                                className='
                                    w-full pt-1.5
                                    md:pt-2
                                    lg:pt-2.5
                                '>
                                <MakeBlog
                                    field={_key}
                                    value={value[_key]}
                                />
                            </div>
                        ) :
                        isArray(value) ?
                            <p className={Class.Value}>
                                {value.join(', ')}
                            </p> :
                            isBoolean(value) ?
                                <p className={Class.Value}>
                                    {value ? 'Yes' : 'No'}
                                </p> :
                                isLink(value.toString()) ?
                                    isImageUrl(value) ?
                                        <a
                                            href={value}
                                            rel='noreferrer'
                                            target='_blank'
                                            className='block'>
                                            <Icon
                                                link={value}
                                            />
                                        </a> :
                                        <a
                                            href={value}
                                            rel='noreferrer'
                                            target='_blank'
                                            className={
                                                Class.ValueLink
                                            }>
                                            {value}
                                        </a>
                                    :
                                    <p className={Class.Value}>
                                        {value}
                                    </p>
                }
            </div>
        </div>
    );
}

const OtherInformation = ({ country }: { country: any }) => {
    return (
        <div
            className='
                w-full  flex flex-col gap-y-1 break-all
                 md:gap-y-1.5
                 lg:gap-y-2
            '>
            {
                Object.keys(country).map((_key, index) =>
                    <MakeBlog
                        key={index}
                        field={_key}
                        value={country[_key]}
                    />
                )
            }
        </div>
    );
}

export default OtherInformation;