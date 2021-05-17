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
    <li><a href="#usage">Usage</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
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
If you are deploying the system in a local environment, you can access the page on <http://localhost:5000>. 
Otherwise you can access the page with the IP address or DNS of the server on port 5000. 

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
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_


<!-- CONTACT -->
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Img Shields](https://shields.io)
* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Pages](https://pages.github.com)
* [Animate.css](https://daneden.github.io/animate.css)
* [Loaders.css](https://connoratherton.com/loaders)
* [Slick Carousel](https://kenwheeler.github.io/slick)
* [Smooth Scroll](https://github.com/cferdinandi/smooth-scroll)
* [Sticky Kit](http://leafo.net/sticky-kit)
* [JVectorMap](http://jvectormap.com)
* [Font Awesome](https://fontawesome.com)





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