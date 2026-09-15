---
viewer: false
language:
- en
license: apache-2.0
task_categories:
- robotics
pretty_name: ArtVIP
tags:
- usd
- articulations
- Robotics simulation
Modalities:
- 3D
Formats:
- webdataset
---

# ArtVIP dataset card


[![License](https://img.shields.io/badge/License-Apache_2.0-yellow.svg)](https://opensource.org/licenses/Apache-2.0)
[![Project Page](https://img.shields.io/badge/Project%20Page-ArtVIP-blue.svg)](https://x-humanoid-artvip.github.io/)
[![Hugging Face](https://img.shields.io/badge/Hugging_Face-ArtVIP-yellow.svg)](https://huggingface.co/datasets/x-humanoid-robomind/ArtVIP)
[![arXiv](https://img.shields.io/badge/arXiv-ArtVIP-red.svg)](https://arxiv.org/abs/2506.04941)
[![Paper](https://img.shields.io/badge/Hugging_Face-Paper-yellow.svg)](https://huggingface.co/papers/2506.04941)


## 🎉🎉🎉 ArtVIP is accepted by ICLR 2026

## Key Features 


✅ 476 high-quality digital-twin articulated objects. 
 ![articulated objects](./assets/206_articulated_objects.gif) 

<div align="center" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 2rem 0;">
  
  <!-- Digital Twin Scenes -->
  <div style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <img src="./assets/digital_twin_scences.gif" width="100%" alt="Digital Twin Scenes">
    <p style="text-align: center; margin: 8px 0; font-size: 0.9em; color: #666;">
      ✅ 6 pre-configured digital-twin scenes, 6 user-defined scenes
    </p>
  </div>

  <!-- Reusable Modular Interaction -->
  <div style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <img src="./assets/Magnetic_attraction.gif" width="100%" alt="Modular Interaction">
    <p style="text-align: center; margin: 8px 0; font-size: 0.9em; color: #666;">
      ✅ Reusable Modular interaction
    </p>
  </div>

  <!-- Physics Fidelity -->
  <div style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <img src="assets/chair.gif" width="100%" alt="Physics Fidelity">
    <p style="text-align: center; margin: 8px 0; font-size: 0.9em; color: #666;">
      ✅ Physics fidelity
    </p>
  </div>

  <!-- Pixel-level Affordance Annotations -->
  <div style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <img src="assets/Seg_chair.gif" width="100%" alt="Affordance Annotations">
    <p style="text-align: center; margin: 8px 0; font-size: 0.9em; color: #666;">
      ✅ Pixel-level affordance annotations
    </p>
  </div>

</div>****

---
## [Version History](./assets/Release_history.md) 

[Click here](./assets/Release_history.md) to view historical versions

| Version | Release Date | Description                                                                 | Highlights |
|---------|--------------|-----------------------------------------------------------------------------|------------|
| v1.3    | 2026-06      | Expanded the dataset.                             | ✅ Added new 3D models<br>✅ Increased total articulated models to 476 |
| v1.2    | 2026-03      | Added new asset categories and simplified USD joint control code.           | ✅ Added 37 IKEA furniture assets (`Ikea_furniture`)<br>✅ Added 15 medical equipment assets (`Medical_equipment`)<br>✅ Simplified USD joint control code |
| v1.1    | 2025-08      |  Optimized the details of interactive scenes.                                       | ✅ Modify interactive scene joint drive configuration<br>✅Optimize collision volume decomposition within interactive scenes <br> ✅Including 48 modular interactive objects |
| v1.0    | 2025-06      | Initial release of ArtVIP dataset                                           | ✅ 206 articulated objects<br>✅ 6 interactive scenes<br>✅ 6 digital twin scenes<br> |

### Dataset Information

### Description

[Click here](https://x-humanoid-artvip.github.io/) for a detailed dataset description and full video introduction.

### Dataset Structure

1. **Articulated objects** 
   
   [Click here](./Articulated_objects/README.md) for the introduction to Articulated objects.
  The specific modular-interaction types:

<div align="center" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 2rem 0;">
  <!-- Modular Interaction GIF 1 -->
  <div style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <img src="assets/modular-interaction/Damping_Effect_cabinet.gif" width="100%" alt="Modular Interaction 1">
    <p style="text-align: center; margin: 8px 0; font-size: 0.9em; color: #666;">
      Damping_Effect_cabinet
    </p>
  </div>
  
  <!-- Modular Interaction GIF 2 -->
  <div style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <img src="assets/modular-interaction/Magnetic_Effect_dishwasher.gif" width="100%" alt="Modular Interaction 2">
    <p style="text-align: center; margin: 8px 0; font-size: 0.9em; color: #666;">
      Magnetic_Effect_dishwasher
    </p>
  </div>
  
  <!-- Modular Interaction GIF 3 -->
  <div style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <img src="assets/modular-interaction/Trigger_Interactions_table_2.gif" width="100%" alt="Modular Interaction 3">
    <p style="text-align: center; margin: 8px 0; font-size: 0.9em; color: #666;">
      Trigger_Interactions_table
    </p>
  </div>
  
  <!-- Modular Interaction GIF 4 -->
  <div style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <img src="assets/modular-interaction/Damping_Effect_cabint_2.gif" width="100%" alt="Modular Interaction 4">
    <p style="text-align: center; margin: 8px 0; font-size: 0.9em; color: #666;">
      Damping_Effect_cabint
    </p>
  </div>
  
  <!-- Modular Interaction GIF 5 -->
  <div style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <img src="assets/modular-interaction/Magnetic_Effect_refrigerator.gif" width="100%" alt="Modular Interaction 5">
    <p style="text-align: center; margin: 8px 0; font-size: 0.9em; color: #666;">
      Magnetic_Effect_refrigerator
    </p>
  </div>
  
  <!-- Modular Interaction GIF 6 -->
  <div style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <img src="assets/modular-interaction/Trigger_Interactions_trash_can.gif" width="100%" alt="Modular Interaction 6">
    <p style="text-align: center; margin: 8px 0; font-size: 0.9em; color: #666;">
      Trigger_Interactions_trash_can
    </p>
  </div>
</div>

2. **Scenes**
   
    2.1 Digital Twin Scenes

   📁 ``ArtVIP/Secenes`` contains **6** user-defined digital-twin scenes. 

    - [📘 Introduction to Digital-Twin Scenes](./Scenes/README.md)
  
   
    2.2 Interactive_scene

   📁 ``ArtVIP/Interactive_scene`` contains **6**  pre-configured Interactive scenes.

   - [📘 Introduction to Interactive scenes](./Interactive_scene/README.md)


<div align="center" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 2rem 0;">

  <!-- Kitchen Scene -->
  <div style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <img src="./assets/kitchen-open.gif" width="100%" alt="Kitchen Scene">
    <p style="text-align: center; margin: 8px 0; font-size: 0.9em; color: #666;">
      🔪 Kitchen Scene Interaction
    </p>
  </div>
  <!-- Small Living Room Scene -->
  <div style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <img src="./assets/smalllivingroom_open.gif" width="100%" alt="Small Living Room Scene">
    <p style="text-align: center; margin: 8px 0; font-size: 0.9em; color: #666;">
      📺 Small Living Room Interaction
    </p>
  </div>

  <!-- Kitchen_with_parlor Scene -->
  <div style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <img src="./assets/parlor_open.gif" width="100%" alt="Parlor Scene">
    <p style="text-align: center; margin: 8px 0; font-size: 0.9em; color: #666;">
      🛋️ Parlor Scene Interaction
    </p>
  </div>
  <!-- Bedroom Scene -->
  <div style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <img src="./assets/bedroom_open.gif" width="100%" alt="Bedroom Scene">
    <p style="text-align: center; margin: 8px 0; font-size: 0.9em; color: #666;">
      🛏️ Bedroom Scene Interaction
    </p>
  </div>

</div>



---


### How to use 

  - This version is compatible with Isaac-Sim 5.0

1. **Install Isaac Sim 5.0 **  
   
   - Official Documentation: [https://docs.isaacsim.omniverse.nvidia.com/latest/installation/quick-install.html](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/quick-install.html)  

   - Linux Version Download: [https://download.isaacsim.omniverse.nvidia.com/isaac-sim-standalone-5.0.0-linux-x86_64.zip](https://download.isaacsim.omniverse.nvidia.com/isaac-sim-standalone-5.0.0-linux-x86_64.zip)

   - Installation steps:
  
   ```bash
   # Create installation directory
   mkdir ~/isaacsim
   
   # Unzip package (assuming downloaded to ~/Downloads)
   cd ~/Downloads
   unzip "isaac-sim-standalone-5.0.0-linux-x86_64.zip" -d ~/isaacsim
   
   # Run post-installation setup
   cd ~/isaacsim
   ./post_install.sh
   
   # Launch Isaac Sim
   ./isaac-sim.selector.sh

### Examples

**Interaction Demo**:

1. Locate the scene file: `/Interactive_scene/kitchen/Interactive_kitchen.usd`

2. Open in Isaac Sim and click ▶️ PLAY
  
3. **Force Application**:
  
   - Hold `SHIFT + Left Click` and drag to apply external forces (highlighted in green in the demonstration image)
 <!-- ![Oven Articulation](./assets/open_oven.png)  -->

<div align="center" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 2rem 0;">

  <!-- Door Opening -->
  <div style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <video controls muted playsinline width="100%">
      <source src="https://huggingface.co/datasets/x-humanoid-robomind/ArtVIP/resolve/main/assets/open_door.mp4" type="video/mp4">
    </video>
    <p style="text-align: center; margin: 8px 0; font-size: 0.9em; color: #666;">
      🚪 Door Operation
    </p>
  </div>

  <!-- Light Switch -->
  <div style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <video controls muted playsinline width="100%">
      <source src="https://huggingface.co/datasets/x-humanoid-robomind/ArtVIP/resolve/main/assets/turn_on.mp4" type="video/mp4">
    </video>
    <p style="text-align: center; margin: 8px 0; font-size: 0.9em; color: #666;">
      💡 Light Switch Activation
    </p>
  </div>

  <!-- Oven Operation -->
  <div style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <video controls muted playsinline width="100%">
      <source src="https://huggingface.co/datasets/x-humanoid-robomind/ArtVIP/resolve/main/assets/oven_open.mp4" type="video/mp4">
    </video>
    <p style="text-align: center; margin: 8px 0; font-size: 0.9em; color: #666;">
      🔥 Microwave Interaction
    </p>
  </div>

  <!-- Refrigerator Demo -->
  <div style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <video controls muted playsinline width="100%">
      <source src="https://huggingface.co/datasets/x-humanoid-robomind/ArtVIP/resolve/main/assets/open_fridge.mp4" type="video/mp4">
    </video>
    <p style="text-align: center; margin: 8px 0; font-size: 0.9em; color: #666;">
      ❄️ Refrigerator Interaction
    </p>
  </div>
</div>

 **Full Object Interactivity**:

 <div align="center" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 2rem 0;">
  <div style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <img src="./assets/Kitchen_interactive.gif" width="100%" alt="Kitchen Scene Example">
    <p style="text-align: center; margin: 8px 0; font-size: 0.9em; color: #666;">
      🍳 Kitchen Interaction Showcase
    </p>
  </div>
  <div style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <img src="./assets/interactive_largelivingroom.gif" width="100%" alt="Bedroom Scene Example">
    <p style="text-align: center; margin: 8px 0; font-size: 0.9em; color: #666;">
      🛋️ livingroom Interaction Showcase
    </p>
  </div>
    <div style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <img src="./assets/interactive_childrenroom.gif" width="100%" alt="childrenroom Scene Example">
    <p style="text-align: center; margin: 8px 0; font-size: 0.9em; color: #666;">
      🧸 childrenroom Interaction Showcase
    </p>
  </div>
    <div style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <img src="./assets/Interactive_kitchen_with_parlor.gif" width="100%" alt="Bedroom Scene Example">
    <p style="text-align: center; margin: 8px 0; font-size: 0.9em; color: #666;">
      🍽️ kitchen_with_parlor Interaction Showcase
    </p>
  </div>
</div>
