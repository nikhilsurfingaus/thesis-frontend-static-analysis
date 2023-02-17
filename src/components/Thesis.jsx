import React from 'react';
import THESIS from '../assets/Thesis.png';
import { AiFillRead } from 'react-icons/ai';

export const Thesis = () => {
  return (
    <div className='w-full bg-black py-16 px-4' id='report'>
      <div className='max-w-[1240px] mx-auto grid md:grid-cols-2'>
        <div className='flex flex-col justify-center'>
          <p className='text-[#A020F0] font-bold text-xl'>THESIS FINDINGS</p>
          <h1 className='text-white md:text-3xl sm:text-3xl text-2xl font-bold py-2'>
            Current Solidity Static Analysis Tools Suck
          </h1>
          <p className='text-white'>
          The  limitations  of  current Solidity Static Analysis Tools  illuminated  a  lack  of  Bug  Attack  Theme (BAT) coverage, 
          missing logic for new bugs/vulnerabilities, poor compatibility/usability and a lack of a solution 
          for that bug or vulnerability.The project produced 35 Control Flow Diagrams (CFD’s) which extended on the logic of existing vulnerabilities, 
          as well as provided logical violation paths for new vulnerabilities and countermeasures. The CFD logic was implemented within 
          the proposed project Solidity Static Analysis tool  ‘PySolSweep’,  which  overcame  existing  limitations  to integrate  
          increased  BAT  coverage,  improved  compatibility/usability  and  solutions  for vulnerabilities  
          and  countermeasures. ‘PySolSweep’  illuminated Smart Contracts containing large  
          volume  of  medium  and  high  impact  bugs,  vulnerabilities  and countermeasures within the scope of Overflow/Underflow, 
          Syntax and DAO.
          </p>
          <div className='flex flex-col items-center mt-6'>
            <div className='mb-3'>
            <a href="https://github.com/nikhilsurfingaus/ThesisProject-Static-Analysis-Solidity-Smart-Contracts/blob/master/Final%20Thesis.pdf"
             target="_blank" rel="noreferrer">
              <button className='bg-purple-500 text-black w-[200px] rounded-md font-medium py-3 hover:bg-white
               hover:text-black hover:border-white border-2 border-[#A020F0] transition-colors duration-300 flex 
               justify-center items-center'>
                <AiFillRead size={25} className='mr-2' />
                <span>Read Thesis</span>
              </button>
            </a>
            </div>
          </div>
        </div>
        <img className='w-[500px] mx-auto my-4' src={THESIS} alt='/' />
      </div>
    </div>
  );
};
