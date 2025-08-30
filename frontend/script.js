

const API_BASE_URL = 'https://predusk-technologies-assignment-vaibhav.onrender.com';

let allProjects = [];

const profileHeader = document.getElementById('profile-header');
const linksSection = document.getElementById('links-section');
const projectsContainer = document.getElementById('projects-container');
const topSkillsList = document.getElementById('top-skills-list');
const workContainer = document.getElementById('work-container');
const educationContainer = document.getElementById('education-container');
const skillSearchInput = document.getElementById('skill-search');

// This prevents the API from being called on every keystroke
function debounce(func, delay) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
}

const debouncedFilter = debounce(() => {
    filterProjects(skillSearchInput.value); 
}, 300);

document.addEventListener('DOMContentLoaded', fetchAndDisplayProfile);
skillSearchInput.addEventListener('input', debouncedFilter);

async function fetchAndDisplayProfile() {
    try {
        const response = await fetch(`${API_BASE_URL}/profile`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const profile = await response.json();

        allProjects = profile.projects;

        renderProfileHeader(profile);
        renderLinks(profile.links);
        renderProjects(profile.projects);
        renderTopSkills(profile.skills);
        renderWorkExperience(profile.work_experience);
        renderEducation(profile.education);

    } catch (error) {
        console.error("Failed to fetch profile:", error);
        projectsContainer.innerHTML = '<p class="error">Could not load profile data. Is the backend server running?</p>';
    }
}

async function filterProjects(query) {
    if (!query) {
        renderProjects(allProjects);
        return;
    }
    try {
        const response = await fetch(`${API_BASE_URL}/projects?q=${encodeURIComponent(query)}`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const filteredProjects = await response.json();
        renderProjects(filteredProjects);
    } catch (error) {
        console.error("Failed to filter projects:", error);
        projectsContainer.innerHTML = '<p class="error">Error filtering projects.</p>';
    }
}


function renderProfileHeader(profile) {
    profileHeader.innerHTML = `
        <h1>${profile.name}</h1>
        <p>${profile.email}</p>
    `;
}

function renderLinks(links) {
    linksSection.innerHTML = links.map(link => `
        <a href="${link.url}" target="_blank">${link.name}</a>
    `).join(' | ');
}

function renderProjects(projects) {
    if (projects.length === 0) {
        projectsContainer.innerHTML = '<p>No projects found for this skill.</p>';
        return;
    }
    projectsContainer.innerHTML = projects.map(project => `
        <div class="project-card">
            <h3>${project.title}</h3>
            <p>${project.description}</p>
            <div class="project-skills">
                ${project.skills.map(skill => `<span>${skill.name}</span>`).join('')}
            </div>
            <div class="project-links">
                ${project.links.github ? `<a href="${project.links.github}" target="_blank">GitHub</a>` : ''}
            </div>
        </div>
    `).join('');
}

function renderTopSkills(skills) {
    const topSkills = skills.filter(s => s.is_top_skill);
    topSkillsList.innerHTML = topSkills.map(skill => `<li>${skill.name}</li>`).join('');
}

function renderWorkExperience(workItems) {
    workContainer.innerHTML = workItems.map(item => `
        <div class="work-item">
            <h4>${item.position} at ${item.company}</h4>
            <p class="dates">${item.start_date} - ${item.end_date || 'Present'}</p>
            <p>${item.description}</p>
        </div>
    `).join('');
}

function renderEducation(educationItems) {
    educationContainer.innerHTML = educationItems.map(item => `
        <div class="education-item">
            <h4>${item.degree}</h4>
            <p>${item.institution}</p>
            <p class="dates">${item.start_date} - ${item.end_date || 'Present'}</p>
        </div>
    `).join('');
}