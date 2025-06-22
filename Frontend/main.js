
$(document).ready(function () {
  function loopText() {
    $(".text").textillate({
      autoStart: false,
      in: {
        effect: "bounceIn",
        callback: function () {
          // Wait then start out
          setTimeout(function () {
            $(".text").textillate("out");
          }, 1000); // how long to wait after in
        },
      },
      out: {
        effect: "bounceOut",
        callback: function () {
          // Reset and start again
          $(".text").textillate("stop").textillate("in");
        },
      },
    });

    $(".text").textillate("in"); // Start first time
  }

  loopText(); // start the loop
});

$(document).ready(function () {
  function loopText() {
    $(".listen-text").textillate({
      autoStart: false,
      in: {
        effect: "bounceIn",
        callback: function () {
          // Wait then start out
          setTimeout(function () {
            $(".listen-text").textillate("out");
          }, 1000); // how long to wait after in
        },
      },
      out: {
        effect: "bounceOut",
        callback: function () {
          // Reset and start again
          $(".listen-text").textillate("stop").textillate("in");
        },
      },
    });

    $(".listen-text").textillate("in"); // Start first time
  }

  loopText(); // start the loop
});

//for siri like waveform

const siriWave = new SiriWave({
  container: document.getElementById("siri-container"),
  width: window.innerWidth,
  height: 100,
  speed: 0.05,
  amplitude: 0,
  autostart: true,
  style: "ios9", // other option: 'ios'
});

navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
  const audioContext = new (window.AudioContext || window.webkitAudioContext)();
  const source = audioContext.createMediaStreamSource(stream);
  const analyser = audioContext.createAnalyser();
  analyser.fftSize = 512;

  const dataArray = new Uint8Array(analyser.frequencyBinCount);
  source.connect(analyser);

  function animate() {
    requestAnimationFrame(animate);
    analyser.getByteFrequencyData(dataArray);
    const volume = dataArray.reduce((a, b) => a + b) / dataArray.length;
    siriWave.setAmplitude(volume / 20); // tune divisor to match effect
  }

  animate();
});

// my logic behind setting up this object for dinamic switching between various html of the body
// let different_sections = {
//   home: `<section id="Home">
//   <div id="jarvis-hood">
//     <canvas id="canvasOne" class="jarvis-soul" width="700" height="420"></canvas>
//     <div class="square">
//       <span class="circle"></span>
//       <span class="circle"></span>
//       <span class="circle"></span>
//     </div>
//   </div>
//   <h1 class="text">Ask Me Any Thing!</h1>
//   <div class="jarvis-ui">
//     <div class="search-box">
//       <button class="mic-btn" title="Voice Input">
//         <!-- Mic SVG -->
//         <svg height="24" width="24" fill="white" viewBox="0 0 24 24">
//           <path d="M12 14a3 3 0 003-3V5a3 3 0 10-6 0v6a3 3 0 003 3z"></path>
//           <path d="M19 11a7 7 0 01-14 0H3a9 9 0 0018 0h-2z"></path>
//           <path d="M12 17v4m0 0h4m-4 0H8" stroke="white" stroke-width="2" stroke-linecap="round"></path>
//         </svg>
//       </button>

//       <textarea placeholder="Ask me anything..." class="search-input"></textarea>

//       <button class="search-btn" title="Search">
//         <!-- Search SVG -->
//         <svg height="24" width="24" fill="white" viewBox="0 0 24 24">
//           <path d="M21 21l-4.35-4.35M10 18a8 8 0 100-16 8 8 0 000 16z" stroke="white" stroke-width="2" fill="none"
//             stroke-linecap="round" stroke-linejoin="round" />
//         </svg>
//       </button>
//     </div>
//   </div>
//          </section>`,
//   listen: ` <section id="Listen">
//              <div><p class="listen-text">hello sir!</p></div>
//              <div id="siri-container"></div>
//             </section>`,
// };

// // ✅ This function updates app view dynamically
// function updateBodyWithSection(sectionName) {
//   const container = document.getElementById("app-container");

//   if (different_sections[sectionName]) {
//     container.innerHTML = different_sections[sectionName];

//     if (sectionName === "listen") {
//       let audio = new Audio("audio/start_sound.mp3");
//       audio.play();
//     }
//   } else {
//     container.innerHTML = `<section><h1>❌ "${sectionName}" not found!</h1></section>`;
//   }
// }
// updateBodyWithSection("listen");

// // ✅ Expose to Python (so Python can call this)
// eel.expose(updateBodyWithSection);
// //to change the text of listen

