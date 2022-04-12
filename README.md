# Manuals for administrators and developers of cow-data-management



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#access">Access</a></li>
        <li><a href="#stop">Stop</a></li>
        <li><a href="#resume">Resume</a></li>
        <li><a href="#remove">Remove</a></li>
      </ul>
    </li>
    <li><a href="#documentation">Documentation</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Cow-data-management system is a project to manage cow data for a SLU research group. You can insert cow data in both Swedish format and Dutch formant in the system, 
make queries on these data, and check their meta data. 


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

The system is based on Docker containers and managed by Docker Compose. So Docker Compose should be installed before your start. 
* Docker Compose
  ```sh
  sudo apt-get update && sudo apt-get install docker-compose
  ```
Please follow the [post installation instructions](https://docs.docker.com/engine/install/linux-postinstall/) to grant Docker priviledged. 

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Li-Ju666/cow-data-management.git
   ```
2. Start the system
   ```sh
   cd cow-data-management && sudo ./run.sh
   ```

### Access
If you are deploying the system in a local environment, you can access the page on <http://localhost:8000>. 
Otherwise you can access the page with the IP address of the server on port 8000. 

### Stop
To stop the system but keep all data inserted: 
```sh
sudo ./stop.sh
```

### Resume
To resume the system from the a stopped system: 
```sh
sudo ./resume.sh
```
Do not run this script, unless there is a stopped system. 

### Remove
To Stop the system and remove all inserted files: 
```sh
sudo ./clean.sh
```

<!-- USAGE EXAMPLES -->
## Documentations


For more examples and documentations, please refer to the [Documentation](https://github.com/Li-Ju666/cow-data-management/tree/main/Documentation). 




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
