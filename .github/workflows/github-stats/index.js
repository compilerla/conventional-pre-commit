require("dotenv").config();

const fs = require("fs");

const octokit = require("@octokit/core");
const client = new octokit.Octokit({ auth: process.env.GITHUB_TOKEN });

async function searchApi(page) {
    console.log(`Searching page ${page}`);
    return client.request("GET /search/code", {
        q: "compilerla/conventional-pre-commit+in:file+language:yaml",
        per_page: 100,
        page: page
    });
}

async function searchHookUsage() {
    try{
        let page = 1;
        const { _, data } = await searchApi(page++);

        let incomplete = data.incomplete_results;

        while (incomplete) {
            const { h, d } = await searchApi(page++);
            data.items.concat(d.items);
            incomplete = d.incomplete_results;
        }

        console.log("Finished searching");
        return data;
    }
    catch (error) {
        console.log(error);
        return {};
    }
}

function updateReadme(repos, owners) {
    console.log("Updating README");

    const path = "../../../README.md";
    const current = fs.readFileSync(path, "utf-8");

    const pattern = /<!\-\- github_stats starts \-\->.*<!\-\- github_stats ends \-\->/s
    const stats = `:octocat: **${repos} public repos** across :woman_technologist: :man_technologist: **${owners} users/orgs** on GitHub use this hook!`;
    const content = `<!-- github_stats starts -->\n${stats}\n<!-- github_stats ends -->`;

    const updated = current.replace(pattern, content);
    fs.writeFileSync(path, updated, "utf-8");

    console.log("Finished updating README");
}

searchHookUsage().then((data) => {
    const hookRefs = data.items.filter(d => d.name == ".pre-commit-config.yaml");
    const repos = new Set(hookRefs.map(d => d.repository.full_name));
    const owners = new Set(hookRefs.map(d => d.repository.owner.login));

    updateReadme(repos.size, owners.size);
});
