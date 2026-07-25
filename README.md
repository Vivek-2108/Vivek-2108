<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=24&pause=1000&color=39D353&center=true&vCenter=true&width=600&height=50&lines=System.init(%22Vivek-2108%22);;Welcome+to+my+Terminal+Profile;Full+Stack+%26+Competitive+Programmer" alt="Terminal Header Typing SVG" />
</p>

<br>

<p align="center">
  <h3><code>$ cat contributions.sh</code></h3>
  <a href="https://github.com/Vivek-2108">
    <img src="contrib-heatmap.svg" alt="Live GitHub Contribution Heatmap" width="100%" />
  </a>
</p>

<br>

<p align="center">
  <h3><code>$ whoami --verbose</code></h3>
</p>

<table align="center" border="0">
  <tr>
    <td align="center" valign="top">
      <img src="ascii.svg" alt="Animated ASCII Portrait" width="440" />
    </td>
    <td align="center" valign="top">
      <img src="info-card.svg" alt="Neofetch Terminal Profile Card" width="440" />
    </td>
  </tr>
</table>

<br>

### 🚀 `$ ls -la ./featured_projects`

| Project | Description | Tech Stack | Repository |
| :--- | :--- | :--- | :--- |
| **Terminal Profile README Engine** | Autonomous vector graphics profile generator with daily automated data pipelines. | `Python` `SVG` `GitHub Actions` | [View Repository](https://github.com/Vivek-2108/Vivek-2108) |
| **Android & Web Applications** | Full-stack mobile & web applications focused on performance and modern design. | `Java` `React` `Node.js` `Firebase` | [View Repositories](https://github.com/Vivek-2108?tab=repositories) |

<br>

### 🏆 `$ cat cp_stats.sh`

<p align="center">
  <img src="cp-stats.svg" alt="Competitive Programming Statistics (Codeforces & LeetCode)" width="100%" />
</p>

<br>

### 🛠️ `$ neofetch --tech-stack`

<p align="center">
  <img src="https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white" alt="Java" />
  &nbsp;
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  &nbsp;
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript" />
  &nbsp;
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
  &nbsp;
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React" />
  &nbsp;
  <img src="https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white" alt="Node.js" />
  &nbsp;
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL" />
  &nbsp;
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git" />
</p>

<br>

### 🌐 `$ cat profiles.sh`

<p align="center">
  <a href="https://codeforces.com/profile/Code_da_vinci" target="_blank">
    <img src="https://img.shields.io/badge/Codeforces-1F8ACB?style=for-the-badge&logo=codeforces&logoColor=white" alt="Codeforces Profile" />
  </a>
  &nbsp;&nbsp;
  <a href="https://leetcode.com/u/vivekjadhav07/" target="_blank">
    <img src="https://img.shields.io/badge/LeetCode-FFA116?style=for-the-badge&logo=leetcode&logoColor=black" alt="LeetCode Profile" />
  </a>
  &nbsp;&nbsp;
  <a href="https://www.linkedin.com/in/vivek-jadhav-290a39301/" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Profile" />
  </a>
</p>

---

## 🖥️ Terminal Profile Architecture & Self-Hosting Guide

This repository contains a fully automated, self-hosted, terminal-themed GitHub Profile README for **[Vivek-2108](https://github.com/Vivek-2108)**.

All animated visuals are vector SVG graphics generated locally via Python scripts with embedded CSS keyframe animations. It uses **zero JavaScript**, **no third-party stats services**, and **no GitHub Personal Access Tokens**.

---

### 📂 Project Structure

```
Vivek-2108/
├── README.md                           # Terminal profile landing page
├── ascii.svg                           # Self-typing animated ASCII portrait
├── info-card.svg                       # Animated Neofetch-style terminal info card
├── contrib-heatmap.svg                 # Live animated GitHub contribution heatmap SVG
├── cp-stats.svg                        # Codeforces & LeetCode statistics SVG card
│
├── assets/
│   ├── profile.jpg                     # Original input profile image
│   └── prepared.png                    # Preprocessed contrast & background image
│
├── data/
│   ├── contributions.json              # Parsed contribution matrix & streak dataset
│   ├── codeforces.json                 # Live Codeforces rating, rank & solved metrics
│   └── leetcode.json                   # Live LeetCode solved breakdown & contest ranking
│
├── scripts/
│   ├── config.py                       # Single source of truth configuration
│   ├── prep_photo.py                   # Image pre-processing (rembg + CLAHE)
│   ├── make_ascii_svg.py               # Animated monochrome ASCII SVG generator
│   ├── make_info_card.py               # Neofetch info card SVG generator
│   ├── fetch_github_contributions.py   # Web scraper for GitHub contribution graph
│   ├── fetch_codeforces.py             # Official Codeforces REST API stats fetcher
│   ├── fetch_leetcode.py               # Public LeetCode profile & contest fetcher
│   ├── render_heatmap_svg.py           # Animated heatmap SVG generator
│   ├── render_cp_stats_svg.py          # Codeforces & LeetCode stats SVG renderer
│   └── requirements.txt                # Python dependencies
│
└── .github/
    └── workflows/
        └── update-profile.yml          # Daily GitHub Actions cron automation
```

---

### 🚀 Quick Start & Local Execution

```bash
# 1. Environment Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt

# 2. Fetch Live Stats & Render All SVGs
python scripts/fetch_github_contributions.py
python scripts/fetch_codeforces.py
python scripts/fetch_leetcode.py

python scripts/make_ascii_svg.py
python scripts/make_info_card.py
python scripts/render_heatmap_svg.py
python scripts/render_cp_stats_svg.py
```
