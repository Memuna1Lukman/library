import React from 'react'

export default function Header() {
  return (
    <div className='fixed z-50 top-5 left-4 right-4 max-w-5/6 mx-auto drop-shadow-md border-none'>
        <nav className='border-gray-200  px-4 lg:px-6 py-2.5'>
            <div className=' '>
                <ul className='flex flex-row justify-center'>
                    <li className='block py-2 pr-4 pl-3 duration-200 border-gray-100 cursor-pointer'>
                        Home
                    </li>
                    <li className='block py-2 pr-4 pl-3 duration-200 border-gray-100 cursor-pointer'>
                        Genres
                    </li>
                    <li className='block py-2 pr-4 pl-3 duration-200 border-gray-100 cursor-pointer'>
                        Others
                    </li>
                </ul>
            </div>
        </nav>
    </div>
  )
}
