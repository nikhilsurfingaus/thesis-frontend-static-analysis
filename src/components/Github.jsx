import React from 'react';
import InstallMain from './Card';
import { BsGithub } from 'react-icons/bs';

export const Github = () => {
  return (
<div className='w-full bg-black py-16 px-4 flex justify-center' id='github'>
  <div className='max-w-[1240px] mx-auto grid md:grid-cols-2 2xl:mr-[35px] 3xl:mr-[250px] '>
        <div className='flex flex-col justify-center md:pr-16'>
          <p className='text-[#A020F0] font-bold text-xl'>GITHUB</p>
          <h1 className='text-white md:text-3xl sm:text-3xl text-2xl font-bold py-2 text-center'>
            Furthering Blockchain Program Analysis
          </h1>
          <p className='text-white text-center'>
            The contributions of this project on the static analysis of solidity smart contracts included the 
            Control Flow Diagrams extending the logic of existing parse tree infrastructures, as well as proposed 23
            new CFD logic for parse tree infrastructures. 

            The comparative consensus with multiple other static tools experiment validated the credibility 
            of violation path logic for parse trees in bug and vulnerability detection. 
 
            The evaluation included the lack of coverage existing static analysis tools provide against core attacks such as 
            Overflow/Underflow, Syntax and DAO. 

            The evaluation moreover illuminated a worrying insight into the large volume of medium to high risk impact bugs 
            and vulnerabilities present in Ethereum blockchain deployed smart contracts. Thus, this project furthered the 
            knowledge and research in the field of static analysis on Solidity Smart Contracts.
          </p>
          <div className='text-center mt-6'>
              <a href="https://github.com/nikhilsurfingaus/ThesisProject-Static-Analysis-Solidity-Smart-Contracts/blob/master/Poster.pdf" 
              target="_blank" rel="noreferrer">
                <button className='bg-purple-500 text-black w-[200px] rounded-md font-medium my-6 md:my-0 py-3 
                hover:bg-white hover:text-black hover:border-white border-2 border-[#A020F0] transition-colors
                 duration-300 mx-auto flex items-center justify-center'>
                  <BsGithub size={25} className='mr-2' /> <span>Github Repo</span>
                </button>
              </a>
          </div>
        </div>
        <div className='flex justify-center'>
          <div className='mx-auto my-4 text-center'>
            <InstallMain className='w-[500px]' />
          </div>
        </div>
      </div>
    </div>
  );
};
