import React from 'react'
import Typed from 'react-typed';
import blockchain from '../assets/blockchain.mp4'
import './mainStyle.css'
//If Mobile bg=Video else png
import { Link } from "react-scroll";

const HeroSection = () => {
  return (
    <div className='text-white m-0 p-0 relative main z-0 animate__animated animate__fadeIn' id='home'>
        <div className="overlay h-screen"></div>
       <video src={blockchain} autoPlay loop muted className="video" />

      <div className='content max-w-[800px] mt-[-70px] w-full h-screen mx-auto text-center flex flex-col justify-center'>
        <p className='text-[#A020F0] font-bold p-2 md:text-3xl sm:text-1xl'>
          "Blockchain Guardian Angel"
        </p>
        <h1 className='md:text-7xl sm:text-6xl text-4xl font-bold md:py-6'>
         SECURE YOUR SMART CONTRACT
        </h1>
        <div className='flex justify-center items-center'>
          <p className='md:text-5xl sm:text-4xl text-xl font-bold py-4'>
            Static Analysis for
          </p>
          <Typed
          className='md:text-5xl sm:text-4xl text-xl font-bold md:pl-4 pl-2'
            strings={['SOLIDITY', 'SMART', 'CONTRACT', 'CODE']}
            typeSpeed={120}
            backSpeed={140}
            loop
          />
        </div>
        <p className='md:text-2xl text-xl font-bold text-gray-500'>Run a static analysis security audit on your smart contract prior to deployment</p>
        <Link
          to='background'
          spy={true}
          smooth={true}
          offset={-70}
          duration={500}
        >
        <button className='bg-[#A020F0] w-[200px] rounded-md font-medium my-6 mx-auto py-3 text-black hover:bg-white hover:text-black hover:border-white border-2 border-[#A020F0] transition-colors duration-300'>Get Started</button>
        </Link>
      </div>
    </div>
    )
}

export default HeroSection