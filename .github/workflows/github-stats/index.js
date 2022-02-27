require("dotenv").config();

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
