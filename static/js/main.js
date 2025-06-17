console.log("Welcome to my portfolio site!");


new Typed("#typed-text", {
  strings: ["a web developer", "a UI/UX designer", "a mobile app developer", "an AI enthusiast"],
  typeSpeed: 50,
  backSpeed: 25,
  backDelay: 1500,
  loop: true
});


const codeLines = [
  "public class Main {",
  "  System.out.println(\"Welcome to my website!\");",
  "}"
];

let line = 0;
let char = 0;
const speed = 50;
const codeElement = document.getElementById("animated-code");

function typeCode() {
  if (line < codeLines.length) {
    if (char < codeLines[line].length) {
      codeElement.textContent += codeLines[line].charAt(char);
      char++;
      setTimeout(typeCode, speed);
    } else {
      codeElement.textContent += "\n";
      line++;
      char = 0;
      setTimeout(typeCode, speed);
    }
  }
}

typeCode();


const tabs = document.querySelectorAll('.tab');
const contents = document.querySelectorAll('.tab-content');

tabs.forEach(tab => {
tab.addEventListener('click', () => {
    // Deactivate all tabs
    tabs.forEach(t => t.classList.remove('active'));
    contents.forEach(c => c.classList.remove('active'));

    // Activate clicked tab and its content
    tab.classList.add('active');
    document.getElementById(tab.dataset.tab).classList.add('active');
});
});

