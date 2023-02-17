import React from 'react';
import SOL from '../assets/Solidity.png';
import { VscFilePdf } from 'react-icons/vsc';

export const Background = () => {
  return (
    <div className='w-full bg-white py-16 px-4' id='background'>
      <div className='max-w-[1240px] mx-auto grid md:grid-cols-2 2xl:mr-[235px] 3xl:mr-[480px] '>
        <img className='w-[800px] mx-auto my-4 
        animate__animated animate__bounce animate__slower animate__delay-2s animate__infinite ' src={SOL} alt='/' />
        <div className='flex flex-col justify-center'>
          <p className='text-[#A020F0] font-bold text-xl'>STATIC ANALYSIS BACKGROUND</p>
          <h1 className='md:text-4xl sm:text-3xl text-2xl font-bold py-2'>
            Verify Code Before Deployement
          </h1>
          <p>
            Static Analysisis a Program Analysismethod applied to programming language code,
            to detect bugs, vulnerabilities and potential countermeasures within code. One
            vulnerable language of Ethereum Smart Contracts, written in Solidity. These attacks
            can be grouped into Overflow/Underflow, Syntax and (DAO). This type of Whiteboxtesting
            works by comparing source code to a set of predefined rules in an automated process.
            With the main objective of achieving software security requirements of confidentiality,
            integrity, authenticity, availability and non-repudiation
          </p>
          <div className='text-center mt-6'>
            <a href="https://github.com/nikhilsurfingaus/ThesisProject-Static-Analysis-Solidity-Smart-Contracts/blob/master/Poster.pdf" target="_blank" rel="noreferrer">
              <button className='bg-purple-500 text-black w-[200px] rounded-md font-medium my-6 md:my-0 py-3
              hover:bg-white hover:text-black hover:border-2 hover:border-solid hover:border-[#A020F0] 
              transition-colors duration-300'>
                <div className='flex items-center justify-center'>
                  <VscFilePdf size={25} className='mr-2' />
                  <span>Summary</span>
                </div>
              </button>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};
