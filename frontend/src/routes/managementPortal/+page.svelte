<script>
  import 'carbon-components-svelte/css/all.css';
  import { Theme } from 'carbon-components-svelte';
  let theme;

  export let user = null;
  // export let user = {groups: ['merlin-admin'], username: "guest"};

  //SIDE NAV BAR AND TOP NAV BAR
  import {
    Header,
    HeaderNav,
    HeaderNavItem,
    HeaderNavMenu,
    SideNav,
    SideNavItems,
    SideNavMenu,
    SideNavMenuItem,
    SideNavLink,
    SideNavDivider,
    SkipToContent,
    Content,
    Grid,
    Row,
    Column,
    Loading
  } from 'carbon-components-svelte';
  import {
    ComposedModal,
    ModalHeader,
    ModalBody,
    ModalFooter,
    TextInput
  } from 'carbon-components-svelte';
  import Home from '~icons/carbon/home';
  import FormEditor from '~icons/icon-park-outline/file-settings-one';
  import Pages from '~icons/mingcute/documents-line';
  import Forms from '~icons/iconoir/page-edit';
  import EntityLink from '~icons/carbon/direct-link';
  import Manage from '~icons/fa6-solid/screwdriver-wrench';
  // import EntityTypes from '~icons/system-uicons/hierarchy';
  import EntityTypes from '~icons/entypo/flow-tree';
  import Analytics from '~icons/majesticons/analytics-line';
  import Deployment from '~icons/icon-park-outline/connection-point';
  import TestAgent from '~icons/clarity/talk-bubbles-line';

  let isSideNavOpen = false;

  //CONTENT TOP MENU > SAVE / CANCEL BUTTONS ETC
  import { Tile, Modal } from 'carbon-components-svelte';

  import DisplayProjects from '$lib/components/DisplayProjects.svelte';
  import DisplayAgents from '$lib/components/DisplayAgents.svelte';
  import AgentDetails from '$lib/components/AgentDetails.svelte';

  //SVELTE VIEWPORT COMPONENT
  import { fade } from 'svelte/transition';
  import View0 from '../+layout.svelte';
  import View1 from '$lib/components/FormListTable.svelte';
  import View3 from '$lib/components/FormFieldsDragNDrop.svelte';
  import View2 from '$lib/components/EntityTypes.svelte';
  import View5 from '$lib/components/Entities.svelte';  //TEMP PUT IN MANAGE TAB FOR EASIER NAVIGATION
  import View4 from '$lib/components/AnalyticsPage.svelte';
  import View6 from '$lib/components/FieldToEntityRelation.svelte';
  import View7 from '$lib/components/TestAgent.svelte';
  const views = [View0, View1, View2, View3, View4, View5, View6, View7];

  let viewportComponent = null;
  let currentView = 0;
  let editingItem = null;
  $: console.log('EDITING ITEM: ' + JSON.stringify(editingItem));

  //FOR CHECKING BEFORE NAVIGATING AWAY
  let originalJSON;
  let newJSON;
  let switchComponent;

  $: switchComponentListener(switchComponent);

  function switchComponentListener(switchTo) {
    console.log('SWITCHING TO COMPONENT:' + switchTo);
    if (switchTo === 'formFields') 
      toggleView(3);
    else if (switchTo === 'entityEditor') 
      toggleView(5);
  }

  let isModalOpen = false; //FOR MODAL
  let pendingViewNumber = 0;

  function toggleView(viewNumber) {
    //CHECK IF CHANGES UNSAVED
    let unsavedChanges = checkforChanges(originalJSON, newJSON);
    if (unsavedChanges === false) 
      currentView = viewNumber;
    else {
      //MODAL TO ABANDON CHANGES
      pendingViewNumber = viewNumber;
      isModalOpen = true;
    }
    //TODO: select corresponding item on sidenavmenu
  }
  function leavePage() {
    currentView = pendingViewNumber;
    isModalOpen = false;
  }
  function updateViewportComponent() {
    viewportComponent = views[currentView];
    console.log(user.groups);
  }
  updateViewportComponent();

  //FOR PAGE REFRESH OR LEAVING APP PAGE
  function beforeUnload() {
    let unsavedChanges = checkforChanges(originalJSON, newJSON);
    if (unsavedChanges === true) {
      event.preventDefault();
      event.returnValue = '';
      return '';
    }
  }

  function checkforChanges(originalData, newData) {
    console.log('OLD: ' + JSON.stringify(originalData));
    console.log('NEW: ' + JSON.stringify(newData));

    if (JSON.stringify(originalData) === JSON.stringify(newData)) 
      return false;
    else {
      console.log('CHANGES UNSAVED');
      return true;
    }
  }

  //PROJECT AND AGENT SELECTION
  import { ProjectsAndAgents } from '$lib/stores';

  let projectList;
  function getProjects() {
    projectList = [];
    $ProjectsAndAgents.forEach((ProjectAndAgents) => {
      projectList.push(ProjectAndAgents.project);
    });
  }
  getProjects();

  let agentList;
  function getAgentsInProject(project) {
    // console.log(project)
    if (project === 'Create New Project') {
      selectedProject = '0';
      modalForNewProject();
    } else {
      agentList = [];
      selectedAgent = '0'; //RESET TO ASK TO SELECT
      $ProjectsAndAgents.forEach((ProjectAndAgents) => {
        if (project === ProjectAndAgents.project) 
          agentList = ProjectAndAgents.agents;
      });
    }
  }

  let isComposedModalOpen = false;
  let newName = '';
  function modalForNewProject() {
    isComposedModalOpen = true;
  }
  function addNewProject() {
    console.log('Creating new project: ' + newName);
    //TODO ADDING HERE

    isComposedModalOpen = false;
    newName = '';
  }

  let selectedProject = '0';
  let selectedAgent = '0';
  $: getAgentsInProject(selectedProject);

  import { Select, SelectItem } from 'carbon-components-svelte';

  //AFTER AGENT SELECTED --- LOAD FORM TEMPLATES TO POPULATE SIDE NAV BAR
  import { apiGetAllFormTemplates } from '$lib/stores'
	import { formsLocal } from '$lib/stores';	//FALLBACK - LIST OF FORMS
	async function getAllFormTemplates() {
		//API CALL
		console.log('API CALL: GET ALL FORM TEMPLATES');

		try {
			const response = await fetch(apiGetAllFormTemplates);
			const getFormTemplates = await response.json();

			if (response.ok) {
				let resultStr = JSON.stringify(getFormTemplates);
				console.log(new Date().toUTCString() + ' RETURNED FORM TEMPLATES RESULT: ' + resultStr);
				//CHANGE DATA
				let transformedData = [];
				getFormTemplates.forEach((formTemplate, index) => {
					transformedData.push({
						id: formTemplate.id, 
						arrID: index,
						form_name: formTemplate.form_name,
					})
				})
				return transformedData;
			} else {
				let getLocalData = useLocalData();
				return getLocalData;
			}
		} catch (error) {
			console.log('FORM TEMPLATES ERROR: ' + error);
			let getLocalData = useLocalData();
			return getLocalData;
		}
	}
	let allFormTemplates = [];
  function useLocalData() {
		console.log('FORM TEMPLATES RESPONSE NOT OK');
		console.log('USING LOCAL DEFINED formsLocal');
		//CHANGE DATA
		let transformedData = [];
		$formsLocal.forEach((formTemplate, index) => {
			transformedData.push({
				id: formTemplate.id, 
				arrID: index,
				form_name: formTemplate.form_name, 
			})
		})
		return transformedData;
	}
  $: getFormsInAgent(selectedAgent)
  function getFormsInAgent(agent) {
    if(agent !== '0')
      allFormTemplates = getAllFormTemplates(); //TODO: WAIT DB DATA UP USE AGENT ID
  }
</script>

<svelte:window on:beforeunload={beforeUnload} />

<!-- MODAL FOR WARNING UNSAVED CHANGES -->
<Modal
  danger
  bind:open={isModalOpen}
  modalHeading="Discard changes?"
  primaryButtonText="Leave the page"
  on:click:button--primary={() => {
    leavePage();
  }}
  secondaryButtonText="Stay on the page"
  on:click:button--secondary={() => (isModalOpen = false)}
  on:open
  on:close
  on:submit
>
  <p>You have unsaved changes. Leave the page?</p>
</Modal>

<!-- MODAL FOR PROJECT CREATION -->
<ComposedModal
  open={isComposedModalOpen}
  on:close={() => (isComposedModalOpen = false)}
  on:submit={() => addNewProject()}
>
  <ModalHeader label="+ New" title="Create New Project" />
  <ModalBody hasForm>
    <TextInput labelText="Enter New Project Name" bind:value={newName} />
  </ModalBody>
  <ModalFooter primaryButtonText="Create" primaryButtonDisabled={newName === ''} />
</ComposedModal>

<!-- TOP NAV BAR -->
<Header company="ST Engineering" platformName="Project Merlin" bind:isSideNavOpen>
  <div class="w-9 max-h-fit absolute ml-4">
    <svg viewBox="0 0 322 354" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect width="322" height="354" fill="white"/>
      <path d="M100.912 314.253L92.6223 287.241H92.4103C92.4417 287.885 92.4888 288.858 92.5516 290.161C92.6301 291.449 92.7008 292.822 92.7636 294.283C92.8264 295.743 92.8578 297.062 92.8578 298.239V314.253H86.3343V279.823H96.2726L104.421 306.152H104.562L113.205 279.823H123.144V314.253H116.338V297.956C116.338 296.873 116.353 295.625 116.385 294.212C116.432 292.799 116.487 291.457 116.55 290.185C116.612 288.897 116.659 287.932 116.691 287.288H116.479L107.6 314.253H100.912ZM142.125 287.429C144.559 287.429 146.655 287.9 148.413 288.842C150.172 289.769 151.53 291.119 152.488 292.893C153.445 294.667 153.924 296.834 153.924 299.393V302.879H136.944C137.023 304.904 137.627 306.497 138.758 307.659C139.904 308.805 141.49 309.378 143.515 309.378C145.195 309.378 146.733 309.206 148.131 308.86C149.528 308.515 150.965 307.997 152.441 307.306V312.864C151.137 313.508 149.771 313.979 148.343 314.277C146.93 314.575 145.211 314.724 143.185 314.724C140.548 314.724 138.208 314.238 136.167 313.264C134.142 312.291 132.548 310.807 131.386 308.813C130.24 306.819 129.667 304.307 129.667 301.277C129.667 298.2 130.185 295.641 131.222 293.6C132.273 291.543 133.734 290.004 135.602 288.984C137.47 287.948 139.645 287.429 142.125 287.429ZM142.173 292.54C140.775 292.54 139.613 292.987 138.687 293.882C137.776 294.777 137.25 296.182 137.109 298.098H147.189C147.173 297.03 146.977 296.08 146.6 295.248C146.239 294.416 145.689 293.757 144.951 293.27C144.229 292.783 143.303 292.54 142.173 292.54ZM174.46 287.429C174.821 287.429 175.237 287.453 175.708 287.5C176.195 287.531 176.588 287.579 176.886 287.641L176.344 294.377C176.109 294.298 175.771 294.243 175.332 294.212C174.908 294.165 174.539 294.141 174.225 294.141C173.298 294.141 172.396 294.259 171.516 294.495C170.653 294.73 169.876 295.115 169.185 295.649C168.494 296.167 167.945 296.857 167.536 297.721C167.144 298.569 166.948 299.613 166.948 300.853V314.253H159.765V287.924H165.205L166.265 292.351H166.618C167.136 291.457 167.78 290.64 168.549 289.902C169.334 289.149 170.221 288.552 171.21 288.112C172.215 287.657 173.298 287.429 174.46 287.429ZM188.85 314.253H181.667V277.609H188.85V314.253ZM203.592 287.924V314.253H196.409V287.924H203.592ZM200.013 277.609C201.08 277.609 201.999 277.86 202.768 278.362C203.537 278.849 203.922 279.768 203.922 281.118C203.922 282.452 203.537 283.379 202.768 283.897C201.999 284.399 201.08 284.65 200.013 284.65C198.929 284.65 198.003 284.399 197.234 283.897C196.48 283.379 196.103 282.452 196.103 281.118C196.103 279.768 196.48 278.849 197.234 278.362C198.003 277.86 198.929 277.609 200.013 277.609ZM226.107 287.429C228.917 287.429 231.178 288.199 232.889 289.737C234.6 291.26 235.456 293.71 235.456 297.085V314.253H228.273V298.875C228.273 296.991 227.928 295.57 227.237 294.612C226.562 293.655 225.494 293.176 224.034 293.176C221.836 293.176 220.337 293.921 219.536 295.413C218.735 296.905 218.335 299.055 218.335 301.866V314.253H211.152V287.924H216.639L217.605 291.292H218.005C218.57 290.381 219.269 289.643 220.101 289.078C220.949 288.513 221.883 288.097 222.904 287.83C223.94 287.563 225.007 287.429 226.107 287.429Z" fill="#2C0D02"/>
      <g style="mix-blend-mode:multiply">
      <path d="M82.001 243.975V34C92.8565 38.064 120.456 54.3202 169.524 115.281C218.591 176.241 236.014 223.655 240.763 243.975H82.001Z" fill="#363FF2"/>
      </g>
      <g style="mix-blend-mode:multiply">
      <path d="M240.762 243.975V69.8491C229.906 73.2193 183.092 100.895 151.204 138.69C119.316 176.484 86.7492 227.124 81.9999 243.975H240.762Z" fill="#FD665F"/>
      </g>
      <path d="M163.531 194.28L160.66 178.694L179.031 196.952L175.012 211.202L188.513 251.408L134.252 257.07L152.049 211.202L163.531 194.28Z" fill="white"/>
    </svg>
  </div>  
  <svelte:fragment slot="skip-to-content">
    <SkipToContent />
  </svelte:fragment>
  <HeaderNav>
    <!-- <HeaderNavItem href="/" text="Link 1" />
    <HeaderNavItem href="/" text="Link 2" />
    <HeaderNavItem href="/" text="Link 3" /> -->
    <!-- <HeaderNavMenu text="Project A">
      <HeaderNavItem href="/" text="Link 1" />
      <HeaderNavItem href="/" text="Link 2" />
      <HeaderNavItem href="/" text="Link 3" />
    </HeaderNavMenu> -->
    <Select
      size="sm"
      bind:selected={selectedProject}
      on:change={(e) => console.log('Project selected: ', e.detail)}
    >
      <SelectItem value="0" text="Select a project" disabled hidden />
      {#each projectList as project}
        <SelectItem value={project} />
      {/each}
    </Select>
    {#if selectedProject !== '0'}
      <Select
        class="ml-2"
        size="sm"
        bind:selected={selectedAgent}
        on:change={(e) => console.log('Agent selected: ', e.detail)}
      >
        <SelectItem value="0" text="Select an agent" disabled hidden />
        {#each agentList as agent}
          <SelectItem value={agent} />
        {/each}
      </Select>
    {/if}
  </HeaderNav>
  <div class="absolute right-0 mr-6 flex items-center text-white">
    <span class="mr-1">Dark mode: </span>
    <Theme
      bind:theme
      render="toggle"
      toggle={{
        themes: ['g10', 'g80'], //g10: light, g80: dark
        labelA: ' ',
        labelB: ' ',
        hideLabel: true,
        size: 'sm'
      }}
    />
    <span class="ml-4">Welcome, {user.username}!</span>
  </div>
</Header>

{#if selectedProject !== '0' && selectedAgent !== '0'}
  <!-- SIDE NAV BAR -->
  <SideNav bind:isOpen={isSideNavOpen} rail>
    <SideNavItems>
      <SideNavLink
        icon={Home}
        text="Home"
        href="/"
        isSelected
        class="!text-black"
        on:click={() => {
          toggleView(0);
        }}
      />
      <SideNavMenu
        icon={FormEditor}
        width="50"
        height="50"
        text="Form Editor"
        on:click={() => {
          // toggleView(1);
        }}
        class="!text-black"
      >
        <!-- <SideNavMenu icon={FormEditor} text="Form Editor"> -->
        <SideNavMenuItem
          href="/"
          on:click={() => {
            toggleView(1);
          }}
        >
          <div class="flex items-center !text-black"><Pages /><span class="ml-2">Forms</span></div>
        </SideNavMenuItem>
        <SideNavDivider />
        {#await allFormTemplates}
          <Loading class="ml-5"withOverlay={false} small description="Retrieving list of entity types..."/>
        {:then formTemplatesData}
          {#each formTemplatesData as form}
            <SideNavMenuItem
              href="/"
              on:click={() => {
                toggleView(3);
                editingItem = {"itemType":"formTemplate","id":form.id}
              }}
            >
              <div class="flex items-center !text-black">
                <Forms /><span class="ml-2">{form.form_name}</span>
              </div>
            </SideNavMenuItem>
          {/each}
        {:catch error}
          Error
        {/await}
      </SideNavMenu>
      <SideNavLink
        icon={EntityLink}
        text="Field-to-entity relationship"
        href="/"
        class="!text-black"
        on:click={() => {
          toggleView(6);
        }}
      />
      <SideNavDivider />
      <!-- <SideNavLink
        icon={Manage}
        text="Manage"
        href="/"
        class="!text-black"
        on:click={() => {
          toggleView(5);
        }}
      /> -->
      <SideNavLink
        icon={EntityTypes}
        text="Entity Types"
        href="/"
        on:click={() => {
          toggleView(2);
        }}
        class="!text-black"
      />
      <SideNavLink
        icon={TestAgent}
        text="Test Agent"
        href="/"
        on:click={() => {
          toggleView(7);
        }}
        class="!text-black"
      />
      <SideNavLink icon={Deployment} text="Deployment" href="/" class="!text-black" />
      <SideNavLink
        icon={Analytics}
        text="Analytics"
        href="/"
        on:click={() => {
          toggleView(4);
        }}
        class="!text-black"
      />
    </SideNavItems>
  </SideNav>
{/if}

<Content id="mainContentDiv" class="!p-0 overflow-x-hidden !mt-0 !pt-[2.78rem]">
  <!-- hide overflow -->
  <Grid class="!p-0 !m-0 min-w-[98vw]">
    <!-- overflow to fill the width -->
    <Row>
      <Column>
        {#if currentView === 0}
          <!-- CONTENT TOP MENU > SAVE / CANCEL BUTTONS ETC -->
          <Tile class="!flex items-center">
            <h3>Hello!</h3>
          </Tile>
          <div class="text-center">
            {#if user}
              <h1>Welcome to Merlin, {user.username}</h1>
              {#if user.groups}
                <p>You are part of the following groups:</p>
                <ul>
                  {#each user.groups as group}
                    <li>{group}</li>
                  {/each}
                </ul>
                <br />
                {#if selectedProject === '0' && selectedAgent === '0'}
                  <span class="font-bold">Select your project and agent to continue...</span>
                {:else if selectedAgent === '0'}
                  Selected Project: {selectedProject}
                  <br />
                  <span class="font-bold">Select your agent to continue</span>
                {:else}
                  Selected Project: {selectedProject}
                  <br />
                  Selected Agent: {selectedAgent}
                {/if}
              {/if}
            {:else}
              <h1>Welcome to Merlin</h1>
            {/if}
          </div>

          {#if selectedProject === '0'}
            <DisplayProjects bind:user bind:selectedProject bind:projects={projectList} />
          {:else if selectedAgent === '0'}
            <DisplayAgents bind:selectedAgent bind:agents={agentList} />
          {:else}
            <AgentDetails bind:localAgentDetail={originalJSON} bind:newAgentDetail={newJSON} />
          {/if}
        {/if}

        <!-- SVELTE VIEWPORT COMPONENT: overflow-auto to scroll inner content only -->
        {#if viewportComponent == views[currentView]}
          <div id="viewport" class="" on:outroend={updateViewportComponent} transition:fade>
            <svelte:component
              this={viewportComponent}
              bind:originalData={originalJSON}
              bind:newData={newJSON}
              bind:switchComponent
              bind:editingItem
              bind:mainTheme={theme}
            />
          </div>
        {/if}
      </Column>
    </Row>
  </Grid>
</Content>

<style>
  :global(.bx--header__name--prefix) {
    left: 109em;
    position: relative;
  }
  :global(.bx--header__name) {
    left: -3em;
    position: relative;
  }
  :global(a.bx--side-nav__link[aria-current='page']
      .bx--side-nav__icon
      > svg, a.bx--side-nav__link[aria-current='page']
      .bx--side-nav__link-text, a.bx--side-nav__link--current
      .bx--side-nav__icon
      > svg, a.bx--side-nav__link--current .bx--side-nav__link-text) {
    color: #0f62fe;
  }
  :global(.bx--side-nav__items) {
    padding-top: 0;
  }
  :global(a.bx--side-nav__link, .bx--side-nav a.bx--header__menu-item, .bx--side-nav
      .bx--header__menu-title[aria-expanded='true']
      + .bx--header__menu, .bx--side-nav__submenu) {
    min-height: 4rem;
    padding-left: 0.8rem;
  }
  :global(.bx--side-nav__menu a.bx--side-nav__link) {
    height: 3rem;
    min-height: 3rem;
    padding-left: 2rem !important;
  }
  :global(.bx--side-nav__icon > svg) {
    width: 1.5rem;
    height: 1.5rem;
  }
</style>
