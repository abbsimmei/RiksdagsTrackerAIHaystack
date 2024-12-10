<template>
    <div>
        <div class="p-10">
            <div class="p-10 bg-blue-50 rounded-lg">
                <input class="border-2 p-2 h-14 w-full" v-model="question" @keyup.enter="handleEnter"
                    placeholder="Type your question and press Enter" />
            </div>
        </div>
        <div class="p-10">
            <div v-for="(answer, index) in answers.slice().reverse()" :key="index" v-html="renderMarkdown(answer)"
                class="p-2 my-2 bg-gray-100 rounded">
            </div>
        </div>
    </div>
</template>

<script setup lang="js">
import { ref } from 'vue';
import { marked } from 'marked'; // Importing the Markdown parser

// Reactive variables
const question = ref("");
const answers = ref([]);

// Original fetch function
async function fetchAI(url) {
  return await fetch(url);
}

// Main function to fetch data
async function main(question) {
    const response = await fetchAI("http://127.0.0.1:8000/fraga/" + question);
    const data = await response.json(); // Parse JSON response
    answers.value.push(data.answer); // Push the answer into the array
    console.log(data); // Log the full response for debugging
}

// Handle Enter key press
function handleEnter() {
  if (question.value.trim() !== "") {
    main(question.value); // Call main with the input value
    question.value = ""; // Clear input field
  } else {
    console.warn("Input is empty. Please provide a valid question.");
  }
}

// Function to render Markdown
function renderMarkdown(markdown) {
  return marked(markdown); // Convert Markdown to HTML
}
</script>
