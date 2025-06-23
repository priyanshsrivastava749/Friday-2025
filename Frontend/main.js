


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
//listen wala text hai temporarily hataya hai
// $(document).ready(function () {
//   function loopText() {
//     $(".listen-text").textillate({
//       autoStart: false,
//       in: {
//         effect: "bounceIn",
//         callback: function () {
//           // Wait then start out
//           setTimeout(function () {
//             $(".listen-text").textillate("out");
//           }, 1000); // how long to wait after in
//         },
//       },
//       out: {
//         effect: "bounceOut",
//         callback: function () {
//           // Reset and start again
//           $(".listen-text").textillate("stop").textillate("in");
//         },
//       },
//     });

//     $(".listen-text").textillate("in"); // Start first time
//   }

//   // loopText(); // start the loop
// });

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



// //to dynamically change the visibility
// // main.js
// function showSection(sectionToShowId) {
//   const sections = ["Home", "Listen"];
//   sections.forEach((id) => {
//     const section = document.getElementById(id);
//     if (id === sectionToShowId) {
//       section.classList.remove("invisible-section");
//     } else {
//       section.classList.add("invisible-section");
//     }
//   });
// }

// window.showSection = showSection;
// eel.expose(showSection);

// // JS ready message to Python
// eel.js_ready_ack(); // ← yeh chalega jaise hi DOM + JS ready ho jaye

// Expose JS function to Python
function showSection(sectionToShowId) {
  const sections = ["Home", "Listen"];
  sections.forEach((id) => {
    const section = document.getElementById(id);
    if (id === sectionToShowId) {
      section.classList.remove("invisible-section");
    } else {
      section.classList.add("invisible-section");
    }
  });
}
window.showSection = showSection;
eel.expose(showSection);

function updateListenText(newText, holdDuration = 5000) {
  console.log("📢 updateListenText called with:", newText);

  const el = document.querySelector(".listen-text");
  if (!el) return console.warn("❌ .listen-text not found");

  // Step 1: Apply text and clear any animations
  el.innerText = newText;
  el.style.opacity = 1;
  el.style.transform = "translateY(20px)";
  el.classList.remove("softBounceInUp", "softFadeOutDown");

  // Step 2: Force DOM reflow to reset animation
  void el.offsetWidth;

  // Step 3: Trigger entry animation
  el.classList.add("softBounceInUp");

  // Step 4: Exit animation after holdDuration
  setTimeout(() => {
    el.classList.remove("softBounceInUp");
    void el.offsetWidth; // again reflow
    el.classList.add("softFadeOutDown");
  }, holdDuration);
}


// Expose function to Python
window.updateListenText = updateListenText;
eel.expose(updateListenText);

