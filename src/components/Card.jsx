import React from 'react'
import { UserCard } from 'react-ui-cards';
import { useEffect , useState} from 'react';
import axios from 'axios';
import { Typography} from "antd";
import "react-tooltip/dist/react-tooltip.css";
import { Tooltip as ReactTooltip } from "react-tooltip";
import {BsFillRecordCircleFill} from 'react-icons/bs'
import './Card.css'

const { Title } = Typography;

function InstalllMain() {
    const [stat, setStats] = useState([])

    useEffect(() => {
        async function fetchData() {
            try {
                const result = await axios(
                    'https://api.github.com/users/nikhilsurfingaus',
                );
                const test = [{
                            key: '1',
                            name: 'Followers',
                            value: result.data.followers,
                        },
                        {
                            key: '2',
                            name: 'Following',
                            value: result.data.following,
                        },
                        {
                            key: '3',
                            name: 'Repos',
                            value: result.data.public_repos,
                        },   
                    ]
                    setStats(test)
            } catch(err) {
                console.log(err)
            }


          }
          fetchData();

      }, []);


  return (
    <>   
        <div className="prof">
            <div>
            <UserCard
                float
                header='https://thumbs.dreamstime.com/b/technology-background-glowing-d-purple-grid-cyber-technology-high-tech-wire-network-futuristic-wireframe-artificial-intelligence-160299596.jpg'
                avatar='https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Github-desktop-logo-symbol.svg/1024px-Github-desktop-logo-symbol.svg.png'
                name='Nikhil Naik'
                positionName= 'Github Profile'
                stats={stat}
                className="githCard z-10"
                href='https://github.com/nikhilsurfingaus?tab=repositories'
            />
            <div className="unCard">
                <div className="notice">
                    <Title className='update' style={{fontSize: '14px', color:'white'}} level={4}>
                        <BsFillRecordCircleFill className='live text-white' id="staty"/> Stats Pulled By GitHub API
                    </Title>
                </div>
            </div>
        </div>

      </div>
      <ReactTooltip
            anchorId="gith"
            place="top"
            content="GitHub is a code hosting platform for version control and collaboration" 
       />
        <ReactTooltip
            anchorId="staty"
            place="top"
            content="GitHub API Provides Up-to-date GitHub user statistics" 
       />
    </>
  )
}

export default InstalllMain