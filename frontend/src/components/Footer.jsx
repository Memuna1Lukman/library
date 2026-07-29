import React from 'react'
import youtube from '../assets/youTube.svg'
import x from '../assets/twitter.svg'
import linkedIn from '../assets/linkedIn.svg'
import ig from '../assets/instagram.svg'



export default function Footer() {
  return (
    <div className='fixed z-50 bottom-0 left-4 right-4 max-w-5/6 mx-auto drop-shadow-md border-none mb-2'>
        <div className='flex flex-row justify-center gap-4'>
            <img src={youtube} alt="youtube" className='w-8' />
            <img src={x} alt="x" className='w-8' />
            <img src={ig} alt="ig" className='w-8' />
            <img src={linkedIn} alt="linkedin" className='w-8' />
        </div>
    </div>
  )
}
