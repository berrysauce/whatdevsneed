<!--<script>
    /** @type {import('./$types').PageData} */
    export let data = []; // Declare the tools prop
</script>-->

<script>
	import { onMount } from 'svelte';
	import { loop_guard } from 'svelte/internal';

	let data = [];
    let searchQuery = "";

    const base_url = "";
    
    // use when testing locally, also change in onMount
    // const base_url = "https://whatdevsneed.com";

	onMount(async () => {
        let res = await fetch("/api/get/tools/all"); // can't replace this with base_url as it doesn't load the data
        data = await res.json();
	});
                    
    async function handleSearch() {
        if (searchQuery.length == 0) {
            let res = await fetch(f`${base_url}/api/get/tools/all`);
            data = await res.json();
            return;
        } else {
            let res = await fetch(`${base_url}/api/get/search?q=${searchQuery}`);
            data = await res.json();
            return;
        };
    };
</script>

<main>
    <section class="py-4 py-xl-5" style="color: rgb(224,189,7);background: linear-gradient(#323232 64%, rgba(255,255,255,0)), url(&quot;data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24'%3E%3Cg fill='%23e0bd07' fill-opacity='0.7'%3E%3Cpolygon fill-rule='evenodd' points='8 4 12 6 8 8 6 12 4 8 0 6 4 4 6 0 8 4'/%3E%3C/g%3E%3C/svg%3E&quot;), #323232;border-bottom: 2px solid rgb(224,189,7);">
        <div class="container">
            <div class="p-4 p-lg-5">
                <h1 class="display-5" style="font-family: 'Plus Jakarta Sans', sans-serif;letter-spacing: -0.5px;font-weight: 700;color: rgb(224, 189, 7);">what devs need&nbsp;<span style="font-weight: normal !important;">—</span>&nbsp;<span style="color: rgb(224, 189, 7);"><span style="font-weight: normal !important;">Discover developer tools to boost your workflow, without any distractions.</span></span></h1>
                <form style="margin-top: 64px;">
                    <input class="form-control search" type="text" on:input={ handleSearch } bind:value={ searchQuery } style="border-radius: 12px;padding: 10px 30px;padding-left: 14px;font-weight: 600;font-family: 'Plus Jakarta Sans', sans-serif;padding-right: 42px;background: rgb(67,67,67);color: rgb(255,255,255)!important;border: 2px solid rgb(102,102,102);" placeholder="Search for tools" name="search">
                        <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icon-tabler-search float-end" style="color: #8e8e8e!important;font-size: 20px;margin-right: 16px;margin-top: -34px;">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                            <circle cx="10" cy="10" r="7"></circle>
                            <line x1="21" y1="21" x2="15" y2="15"></line>
                        </svg>
                    </form>
                <p style="color: rgb(224,189,7);font-family: 'Plus Jakarta Sans', sans-serif;margin-top: 16px;margin-bottom: 150px;">
                    Made in Germany by <a href="https://berrysauce.me" style="color: inherit;" target="_blank">berrysauce</a> on <a href="https://github.com/berrysauce/whatdevsneed" style="color: inherit;" target="_blank">GitHub</a>
                    <a class="btn btn-primary text-end float-end" role="button" style="margin-top: -4px;color: rgb(224,189,7);background: rgba(255,255,255,0);border-style: none;font-weight: 600;font-family: 'Plus Jakarta Sans', sans-serif;padding: 4px;" href="/add">
                        Add your own tool here
                        <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icon-tabler-arrow-right" style="font-size: 18px;margin-bottom: 2px;margin-left: 5px;">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                            <line x1="5" y1="12" x2="19" y2="12"></line>
                            <line x1="13" y1="18" x2="19" y2="12"></line>
                            <line x1="13" y1="6" x2="19" y2="12"></line>
                        </svg>
                    </a>
                </p>
            </div>
        </div>
    </section>

    <section class="py-4 py-xl-5">
        <div class="container" style="padding: 48px;">
            <div class="row">
                {#if !data || data.length == 0}
                    <section class="py-4 py-xl-5">
                        <div class="container text-center" style="padding: 96px 48px;margin-top: 5vh;margin-bottom: 5vh;"><span class="spinner-border" role="status" style="border-width: 3px;color: rgb(224,189,9);margin-bottom: 16px;"></span>
                            <p style="color: rgb(181,181,181);">Loading tools...</p>
                        </div>
                    </section>
                {:else}
                    {#each data as tool}
                        <div class="col-md-6 col-xl-4" style="margin-bottom: 26px;">
                            <div style="padding: 20px;border-radius: 12px;border: 2px solid rgb(230,230,230);height: 100%;position: relative;">
                                <div class="text-center" style="border-bottom: 2px solid rgb(230,230,230);margin-bottom: 32px;padding-bottom: 32px;margin-top: 16px;height: 100px;">
                                    <img class="img-fluid" src="{ tool.image_url }" loading="lazy" style="border-radius: 8px;max-width: 200px;max-height: 60px;" alt="{ tool.name } Logo">
                                </div>
                                <p>
                                    <a href="https://whatdevsneed.com/category/{ tool.category }" style="color: rgb(224,189,7);font-weight: 500;">
                                        { tool.category }
                                    </a>
                                    <span class="float-end" style="color: rgb(181,181,181);font-weight: 400;">
                                        {#if tool.pricing == "Free"}
                                            <span class="float-end" style="color: rgb(181,181,181);font-weight: 400;"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="1em" height="1em" fill="currentColor" style="font-size: 14px;margin-bottom: 3px;margin-right: 5px;color: rgb(224,189,7);">
                                                <!--! Font Awesome Free 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2022 Fonticons, Inc. -->
                                                <path d="M512 256C512 397.4 397.4 512 256 512C114.6 512 0 397.4 0 256C0 114.6 114.6 0 256 0C397.4 0 512 114.6 512 256zM256 48C141.1 48 48 141.1 48 256C48 370.9 141.1 464 256 464C370.9 464 464 370.9 464 256C464 141.1 370.9 48 256 48z"></path>
                                            </svg>Free (<span data-bs-toggle="tooltip" data-bs-placement="right" style="color: rgb(224,189,7);text-decoration: underline;" title="Completely free, without paid plans">?</span>)</span>
                                        {:else if tool.pricing == "Freemium"}
                                            <span class="float-end" style="color: rgb(181,181,181);font-weight: 400;"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="1em" height="1em" fill="currentColor" style="font-size: 14px;margin-bottom: 3px;margin-right: 5px;color: rgb(224,189,7);">
                                                <!--! Font Awesome Free 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2022 Fonticons, Inc. -->
                                                <path d="M512 256C512 397.4 397.4 512 256 512C114.6 512 0 397.4 0 256C0 114.6 114.6 0 256 0C397.4 0 512 114.6 512 256zM256 64V448C362 448 448 362 448 256C448 149.1 362 64 256 64z"></path>
                                            </svg>Freemium (<span data-bs-toggle="tooltip" data-bs-placement="right" style="color: rgb(224,189,7);text-decoration: underline;" title="Partly free, with free and paid plans">?</span>)</span>
                                        {:else if tool.pricing == "Paid"}
                                            <span class="float-end" style="color: rgb(181,181,181);font-weight: 400;"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="1em" height="1em" fill="currentColor" style="font-size: 14px;margin-bottom: 3px;margin-right: 5px;color: rgb(224,189,7);">
                                                <!--! Font Awesome Free 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2022 Fonticons, Inc. -->
                                                <path d="M512 256C512 397.4 397.4 512 256 512C114.6 512 0 397.4 0 256C0 114.6 114.6 0 256 0C397.4 0 512 114.6 512 256z"></path>
                                            </svg>Paid (<span data-bs-toggle="tooltip" data-bs-placement="right" style="color: rgb(224,189,7);text-decoration: underline;" title="Only paid plans available">?</span>)</span>
                                        {/if}
                                    </span>
                                </p>
                                <p style="font-size: 24px;font-family: 'Plus Jakarta Sans', sans-serif;font-weight: 700;margin-bottom: 8px;">
                                    { tool.name }

                                    {#if tool.staff_pick}
                                        <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 20 20" fill="none" data-bs-toggle="tooltip" data-bss-tooltip="" data-bs-placement="right" style="margin-left: 5px;margin-bottom: 3px;color: #6697e1;" title="Staff-Pick">
                                            <path fill-rule="evenodd" clip-rule="evenodd" d="M6.26701 3.45496C6.91008 3.40364 7.52057 3.15077 8.01158 2.73234C9.15738 1.75589 10.8426 1.75589 11.9884 2.73234C12.4794 3.15077 13.0899 3.40364 13.733 3.45496C15.2336 3.57471 16.4253 4.76636 16.545 6.26701C16.5964 6.91008 16.8492 7.52057 17.2677 8.01158C18.2441 9.15738 18.2441 10.8426 17.2677 11.9884C16.8492 12.4794 16.5964 13.0899 16.545 13.733C16.4253 15.2336 15.2336 16.4253 13.733 16.545C13.0899 16.5964 12.4794 16.8492 11.9884 17.2677C10.8426 18.2441 9.15738 18.2441 8.01158 17.2677C7.52057 16.8492 6.91008 16.5964 6.26701 16.545C4.76636 16.4253 3.57471 15.2336 3.45496 13.733C3.40364 13.0899 3.15077 12.4794 2.73234 11.9884C1.75589 10.8426 1.75589 9.15738 2.73234 8.01158C3.15077 7.52057 3.40364 6.91008 3.45496 6.26701C3.57471 4.76636 4.76636 3.57471 6.26701 3.45496ZM13.7071 8.70711C14.0976 8.31658 14.0976 7.68342 13.7071 7.29289C13.3166 6.90237 12.6834 6.90237 12.2929 7.29289L9 10.5858L7.70711 9.29289C7.31658 8.90237 6.68342 8.90237 6.29289 9.29289C5.90237 9.68342 5.90237 10.3166 6.29289 10.7071L8.29289 12.7071C8.68342 13.0976 9.31658 13.0976 9.70711 12.7071L13.7071 8.70711Z" fill="currentColor"></path>
                                        </svg>
                                    {/if}
                                </p>
                                <p style="color: rgb(181,181,181);margin-bottom: 80px;">
                                    { tool.description }
                                </p>
                                <div style="bottom: 0;position: absolute;margin-bottom: 20px;">
                                    <a class="btn btn-primary" role="button" style="border-radius: 8px;padding: 3px 12px;background: rgba(224,189,7,0);font-weight: 500;font-size: 16px;margin-right: 0px;color: rgb(224,189,7);border: 2px solid rgb(224,189,7);" href="{ tool.tool_url }" target="_blank">
                                        Visit
                                        <svg class="icon icon-tabler icon-tabler-arrow-up-right" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round" style="font-size: 18px;margin-bottom: 1px;margin-left: 3px;">
                                            <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                                            <line x1="17" y1="7" x2="7" y2="17"></line>
                                            <polyline points="8 7 17 7 17 16"></polyline>
                                        </svg>
                                    </a>
                                    <a class="btn btn-primary" role="button" style="border-radius: 8px;padding: 5px 15px;background: rgba(224,189,7,0);border-style: none;font-weight: 500;font-size: 16px;color: rgb(224,189,7);" href="{ tool.share_url }" target="_blank">
                                        Share on Twitter
                                    </a>
                                </div>
                            </div>
                        </div>
                    {/each}
                {/if}
            </div>
        </div>
    </section>
</main>
