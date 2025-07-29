#!/usr/bin/env python3

import streamlit as st
import streamlit.components.v1 as components

st.write("## Polls")
st.warning(":material/warning:This is still under development. Your polls will not be sent into the web. Instead, they will be saved in your browser.")
components.html("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Poll</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Lexend:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Lexend', sans-serif;
        }
    </style>
</head>
<body class="bg-gray-100 flex items-start justify-center p-4 pt-8 pb-8">
    <div class="bg-white p-8 rounded-lg shadow-xl max-w-md w-full border border-gray-200" style="height: 1000px;">
        <h4 class="text-xl font-bold text-gray-800 mb-6 text-center">
            This week's debate: 
        </h4>
        <h1 class="text-3xl font-bold text-gray-800 mb-6 text-center">Is Julia awesome?</h1>

        <div id="poll-options" class="space-y-4 mb-6">
            <!-- Poll options will be dynamically inserted here by JavaScript -->
        </div>

        <div id="message-area" class="text-center text-sm mb-4 h-6"></div>

        <button id="submit-vote" class="w-full bg-blue-600 text-white py-3 rounded-md hover:bg-blue-700 transition duration-300 ease-in-out font-semibold shadow-md">
            Submit Vote
        </button>

        <div id="results-container" class="mt-8 space-y-4">
            <!-- Poll results will be dynamically inserted here by JavaScript -->
        </div>

        <button id="reset-poll" class="w-full bg-red-500 text-white py-2 rounded-md hover:bg-red-600 transition duration-300 ease-in-out font-semibold mt-6 shadow-md">
            Reset Poll
        </button>

        <!-- Custom Confirmation Modal -->
        <div id="confirmation-modal" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center hidden">
            <div class="bg-white p-6 rounded-lg shadow-xl max-w-sm w-full text-center">
                <p class="text-lg font-semibold mb-4">Are you sure you want to reset the poll?</p>
                <div class="flex justify-center space-x-4">
                    <button id="confirm-reset" class="bg-red-500 text-white py-2 px-4 rounded-md hover:bg-red-600 transition duration-300">Yes, Reset</button>
                    <button id="cancel-reset" class="bg-gray-300 text-gray-800 py-2 px-4 rounded-md hover:bg-gray-400 transition duration-300">Cancel</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Define the poll options and their initial vote counts (these would ideally come from the database)
        const pollOptions = {
            "Ummm... Yeah?": 0,
            "Nope": 0,
        };

        // --- IMPORTANT: In a real app, these API endpoints would point to your server-side scripts (e.g., PHP files) ---
        // For demonstration, these are placeholders.
        const API_BASE_URL = 'http://your-infinityfree-domain.com/api/'; // Replace with your actual domain and API path
        const GET_VOTES_ENDPOINT = API_BASE_URL + 'get_votes.php'; // Example PHP file to get votes
        const SUBMIT_VOTE_ENDPOINT = API_BASE_URL + 'submit_vote.php'; // Example PHP file to submit a vote
        const RESET_POLL_ENDPOINT = API_BASE_URL + 'reset_poll.php'; // Example PHP file to reset the poll
        // ---------------------------------------------------------------------------------------------------------

        // Get references to DOM elements
        const pollOptionsContainer = document.getElementById('poll-options');
        const submitVoteButton = document.getElementById('submit-vote');
        const resultsContainer = document.getElementById('results-container');
        const resetPollButton = document.getElementById('reset-poll');
        const messageArea = document.getElementById('message-area');
        const confirmationModal = document.getElementById('confirmation-modal');
        const confirmResetButton = document.getElementById('confirm-reset');
        const cancelResetButton = document.getElementById('cancel-reset');

        // Variable to hold the current poll vote data
        let currentVotes = {};

        /**
         * Loads vote data from a simulated API (would be MySQL in a real backend).
         * If the API call fails, it falls back to local storage.
         */
        async function loadVotes() {
            try {
                // Simulate fetching data from a backend API
                // In a real scenario, this would fetch the current vote counts from your MySQL database via PHP
                const response = await fetch(GET_VOTES_ENDPOINT, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                // Merge with default options to ensure all options are present
                currentVotes = { ...pollOptions, ...data };
                displayMessage('Votes loaded from server (simulated)!', 'success');
            } catch (e) {
                console.error("Could not load votes from server (simulated). Falling back to local storage.", e);
                // Fallback to local storage if API call fails or is not set up
                const storedVotes = localStorage.getItem('pollVotes');
                if (storedVotes) {
                    try {
                        currentVotes = { ...pollOptions, ...JSON.parse(storedVotes) };
                    } catch (parseError) {
                        console.error("Error parsing stored votes, using default.", parseError);
                        currentVotes = { ...pollOptions };
                    }
                } else {
                    currentVotes = { ...pollOptions };
                }
                displayMessage('Using local storage for votes (server not connected)!', 'error');
            }
            renderResults(); // Always render results after attempting to load votes
        }

        /**
         * Saves the current vote data to a simulated API (would be MySQL in a real backend).
         * Also saves to local storage as a fallback/demonstration.
         */
        async function saveVoteToServer(option) {
            try {
                // Simulate sending data to a backend API
                // In a real scenario, this would send the vote to your PHP script, which updates MySQL
                const response = await fetch(SUBMIT_VOTE_ENDPOINT, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ vote: option })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const result = await response.json();
                if (result.success) {
                    displayMessage('Your vote has been submitted to server (simulated)!', 'success');
                    // After successful server update, re-load votes to get the latest state
                    await loadVotes();
                } else {
                    displayMessage('Failed to submit vote to server (simulated).', 'error');
                }
            } catch (e) {
                console.error("Could not submit vote to server (simulated).", e);
                displayMessage('Server not available. Vote only saved locally!', 'error');
                // If server fails, still update local storage for immediate user feedback
                if (currentVotes.hasOwnProperty(option)) {
                    currentVotes[option]++;
                    localStorage.setItem('pollVotes', JSON.stringify(currentVotes));
                }
                renderResults();
            }
        }

        /**
         * Displays a temporary message in the message area.
         * @param {string} message - The message to display.
         * @param {string} type - The type of message (e.g., 'success', 'error').
         */
        function displayMessage(message, type = '') {
            messageArea.textContent = message;
            messageArea.className = `text-center text-sm mb-4 h-6 ${type === 'error' ? 'text-red-600' : 'text-green-600'}`;
            setTimeout(() => {
                messageArea.textContent = '';
                messageArea.className = 'text-center text-sm mb-4 h-6'; // Reset classes
            }, 3000); // Message disappears after 3 seconds
        }

        /**
         * Renders the poll options as radio buttons.
         */
        function renderOptions() {
            pollOptionsContainer.innerHTML = ''; // Clear existing options
            for (const option in pollOptions) { // Use pollOptions for rendering structure
                const label = document.createElement('label');
                label.className = 'flex items-center p-3 rounded-md border border-gray-300 cursor-pointer hover:bg-gray-50 transition duration-200 ease-in-out';
                label.innerHTML = `
                    <input type="radio" name="poll-option" value="${option}" class="form-radio h-5 w-5 text-blue-600 border-gray-300 focus:ring-blue-500 mr-3">
                    <span class="text-gray-700 font-medium">${option}</span>
                `;
                pollOptionsContainer.appendChild(label);
            }
        }

        /**
         * Renders the poll results as a bar chart.
         */
        function renderResults() {
            resultsContainer.innerHTML = ''; // Clear existing results

            const totalVotes = Object.values(currentVotes).reduce((sum, count) => sum + count, 0);

            if (totalVotes === 0) {
                const noResults = document.createElement('p');
                noResults.className = 'text-center text-gray-500 italic';
                noResults.textContent = 'No votes yet. Be the first to vote!';
                resultsContainer.appendChild(noResults);
                return;
            }

            // Sort options by vote count in descending order
            const sortedOptions = Object.entries(currentVotes).sort(([, a], [, b]) => b - a);

            sortedOptions.forEach(([option, count]) => {
                const percentage = totalVotes > 0 ? ((count / totalVotes) * 100).toFixed(1) : 0;

                const resultItem = document.createElement('div');
                resultItem.className = 'mb-4';
                resultItem.innerHTML = `
                    <div class="flex justify-between items-center mb-1">
                        <span class="text-gray-700 font-medium">${option}</span>
                        <span class="text-gray-600 text-sm">${count} vote(s) (${percentage}%)</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
                        <div class="bg-green-500 h-full rounded-full transition-all duration-500 ease-out" style="width: ${percentage}%;"></div>
                    </div>
                `;
                resultsContainer.appendChild(resultItem);
            });
        }

        /**
         * Handles the submission of a vote.
         */
        async function submitVote() {
            const selectedOption = document.querySelector('input[name="poll-option"]:checked');

            if (selectedOption) {
                const vote = selectedOption.value;
                // Update local storage immediately for quick feedback
                if (currentVotes.hasOwnProperty(vote)) {
                    currentVotes[vote]++;
                    localStorage.setItem('pollVotes', JSON.stringify(currentVotes)); // Save to local storage as backup/initial display
                }
                renderResults(); // Render results based on local update

                // Then, attempt to send the vote to the server
                await saveVoteToServer(vote);

                // Deselect the radio button after voting
                selectedOption.checked = false;
            } else {
                displayMessage('Please select an option to vote.', 'error');
            }
        }

        /**
         * Resets the poll to its initial state.
         */
        function resetPoll() {
            // Show the confirmation modal
            confirmationModal.classList.remove('hidden');
        }

        /**
         * Confirms and performs the poll reset via a simulated API call.
         */
        async function confirmResetPoll() {
            try {
                // Simulate sending a reset request to the backend API
                const response = await fetch(RESET_POLL_ENDPOINT, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ action: 'reset' }) // Send a reset action
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const result = await response.json();
                if (result.success) {
                    displayMessage('Poll has been reset on server (simulated)!', 'success');
                    // After successful server reset, re-load votes to get the latest state (all zeros)
                    currentVotes = { ...pollOptions }; // Reset local state
                    localStorage.setItem('pollVotes', JSON.stringify(currentVotes)); // Clear local storage
                    await loadVotes(); // Re-fetch from server to confirm reset
                } else {
                    displayMessage('Failed to reset poll on server (simulated).', 'error');
                }
            } catch (e) {
                console.error("Could not reset poll on server (simulated).", e);
                displayMessage('Server not available. Resetting locally only!', 'error');
                // Fallback to local reset if API fails
                currentVotes = { ...pollOptions }; // Reset to initial counts
                localStorage.setItem('pollVotes', JSON.stringify(currentVotes));
                renderResults();
            } finally {
                confirmationModal.classList.add('hidden'); // Hide modal regardless of success/failure
            }
        }

        /**
         * Initializes the application.
         */
        async function init() {
            renderOptions(); // Render poll options first
            await loadVotes(); // Attempt to load votes from server, then fallback to local storage

            // Event Listeners
            submitVoteButton.addEventListener('click', submitVote);
            resetPollButton.addEventListener('click', resetPoll);

            confirmResetButton.addEventListener('click', confirmResetPoll);

            cancelResetButton.addEventListener('click', () => {
                confirmationModal.classList.add('hidden'); // Hide modal
            });
        }

        // Initialize the app when the DOM is fully loaded
        document.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>
""", height=800)