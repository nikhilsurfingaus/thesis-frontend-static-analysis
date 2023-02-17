import React from 'react';
import py from '../assets/python.png';
import { TbBrandPython } from 'react-icons/tb';

export const Tool = () => {
  return (
    <div className='w-full bg-white py-16 px-4' id='tool'>
      <div className='max-w-[1240px] mx-auto grid md:grid-cols-2 2xl:mr-[200px] 3xl:mr-[400px] '>
        <img className='w-[450px] mx-auto my-4
        animate__animated animate__bounce animate__slower animate__delay-2s animate__infinite' src={py} alt='/' />
        <div className='flex flex-col justify-center'>
          <p className='text-[#A020F0] font-bold text-xl'>TOOL</p>
          <h1 className='md:text-4xl sm:text-3xl text-2xl font-bold py-2'>Verify Code Before Deployment</h1>
          <p>
          PySolSweep is a Static Program Analysis tool, which evaluates the securiity safety of a Solidity based Smart Contract.
           This tool offers coverage accross three classes of attacks from Overflow/Underflow, Syntax and DAO. A total of 35 
           major bugs and their variants are detcted by the Python based Static Analysis tool. This benefits of PySolSweep is 
           its ability to overcome existing Solidity Static Analysis tools limitations and gaps of a systematic approach of Bug 
           Attack Theme coverage of bugs rather than a randmom assortment, suggested solution to overcome bug, vulnrability or 
           countermeasure. As well as new bugs, vulnerbilities and countermeasures discovered from credited Academic Papers 
           reviewed 2020-2022. The tool will not only provide a log report of the Static Analysis results but also give a 
           contract rating score.
          </p>
          <div className='flex flex-col items-center mt-6'>
          <a href="https://github.com/nikhilsurfingaus/ThesisProject-Static-Analysis-Solidity-Smart-Contracts/archive/refs/heads/master.zip" 
          target="_blank" rel="noreferrer">
          <button className='bg-purple-500 text-black w-[200px] rounded-md font-medium py-3
           hover:bg-white hover:text-black hover:border-2 hover:border-solid hover:border-[#A020F0] 
           transition-colors duration-300'>
            <div className='flex items-center justify-center'>
              <TbBrandPython size={25} className='mr-2' />
              <span>Download</span>
            </div>
          </button>
          </a>
          </div>
        </div>
      </div>
    </div>
  );
};
