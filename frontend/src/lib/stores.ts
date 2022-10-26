import { writable } from "svelte/store";

export const ProjectsAndAgents = writable([
  { project: 'Project Merlin', agents: ['Agent 995', 'Agent 999'] },
  { project: 'Project B', agents: ['Agent 1'] },
  { project: 'Project C', agents: ['Agent 2', 'Agent 3'] },
  { project: 'Project D', agents: ['Agent 4', 'Agent 5', 'Agent 6'] },
  { project: 'Project E', agents: ['Agent 7', 'Agent 8', 'Agent 9', 'Agent 10'] }
])

export const agentDetail = writable({
  id: "1",
  name: "Agent 1",
  location: "Singapore (SG)",
  timezone: "Singapore",
  lang: "en - English"
})

export const formsLocal = writable([
    { 
      id: '1', 
      form_name:'Default', 
      numOfFields: '4', 
      version: '1.00', 
      active: false, 
      examples: [
      ], 
      created_at: "2022-10-01T05:42:02.284Z", 
      last_modified: "2022-10-15T11:42:02.284Z" 
    }, 
    { id: '2', form_name:'Fire', numOfFields: '2', version: '1.00', active: false, examples: [
        "fire",
        "burning"
      ], created_at: "2022-10-02T05:42:02.284Z", last_modified: "2022-10-12T15:42:02.284Z" }, 
    { id: '3', form_name:'Medical', numOfFields: '0', version: '1.00', active: false, examples: [
      "ambulance",
      "I need an ambulance",
      "medical help",
      "I need some medical help"
    ], created_at: "2022-10-03T05:42:02.284Z", last_modified: "2022-10-13T15:42:02.284Z" }
])

export const entityTypesLocal = writable([
    { id: "1", entity_type:'caller_name', active: false, created_at: "2022-10-01T05:42:02.284Z", last_modified: "2022-10-09T05:42:02.284Z" }, 
    { id: "2", entity_type:'caller_contact', active: false, created_at: "2022-10-02T05:42:02.284Z", last_modified: "2022-10-10T05:42:02.284Z" }, 
    { id: "3", entity_type:'address', active: false, created_at: "2022-10-03T05:42:02.284Z", last_modified: "2022-10-11T05:42:02.284Z" },
    { id: "4", entity_type:'call_details', active: false, created_at: "2022-10-04T05:42:02.284Z", last_modified: "2022-10-12T05:42:02.284Z" },
    { id: "5", entity_type:'caller_on_site', active: false, created_at: "2022-10-05T05:42:02.284Z", last_modified: "2022-10-13T05:42:02.284Z" },
    { id: "6", entity_type:'medical_category', active: false, created_at: "2022-10-06T05:42:02.284Z", last_modified: "2022-10-14T05:42:02.284Z" },
    { id: "7", entity_type:'medical_symptoms', active: false, created_at: "2022-10-07T05:42:02.284Z", last_modified: "2022-10-15T05:42:02.284Z" },
    { id: "8", entity_type:'fire_keywords', active: false, created_at: "2022-10-08T05:42:02.284Z", last_modified: "2022-10-16T05:42:02.284Z" }
])

export const entityDetailsLocal = writable({
  id: "entity_id_6",  //NOT IN JSON > NEED TO PARSE FROM ENTITY TYPES PAGE
  entity_type: "medical_category",
  entities: [
    { 
      // id: 1, 
      entity: "Medical - Unconscious", 
      synonyms: ["unconscious", "drowsy", "faint"], 
      // active: false, 
      last_modified_timestamp: "2022-10-05T05:42:02.284Z" 
    },
    { 
      // id: 2, 
      entity: "Medical - Bleeding", 
      synonyms: ["blood", "bleed", "red liquid"], 
      // active: false, 
      last_modified_timestamp: "2022-10-10T05:42:02.284Z" 
    }
  ],
  conditions: ["put out"]
})

export const fieldToEntityRelation = writable([
  { arrID: 1, id: 1, value:'@address', field_name: 'Location', form:'Medical', active: false, last_modified_timestamp: "2022-10-10T05:42:02.284Z" },
  { arrID: 2, id: 2, value:'@medical_category', field_name: 'Medical Category', form:'Medical', active: false, last_modified_timestamp: "2022-10-11T05:42:02.284Z" },
  { arrID: 3, id: 3, value:'@medical_symptoms', field_name: 'Medical Symptoms', form:'Medical', active: false, last_modified_timestamp: "2022-10-12T05:42:02.284Z" },
  { arrID: 4, id: 4, value:'@fire_keywords', field_name: 'Fire Keywords', form:'Fire', active: false, last_modified_timestamp: "2022-10-13T05:42:02.284Z" }
])

/*API ENPOINTS*/
// const apiBaseLink = "http://192.168.180.37:27001/forms"  //FOR LOCAL TESTING
const apiBaseLink = "https://dev.merlin.intellism.tech/forms"

//Get all entity types
export let apiGetAllEntityTypes = apiBaseLink + "/v1/entity-types"  //GET
//Create an entity type
export let apiCreateEntityType = apiBaseLink + "/v1/entity-types" //POST 
//Update entity type with ID
export let apiUpdateEntityType = apiBaseLink + "/v1/entity-types" //PUT with /{id}
//Delete entity type with ID
export let apiDeleteEntityType = apiBaseLink + "/v1/entity-types" //DELETE with /{id}
//Get entity type details with ID
export let apiGetEntityTypeDetails = apiBaseLink + "/v1/entity-types"  //GET with /{id}

//Get all form templates
export let apiGetAllFormTemplates = apiBaseLink + "/v1/form-templates"  //GET
//Create a form template
export let apiCreateFormTemplate = apiBaseLink + "/v1/form-templates" //POST 
//Update a form template with ID
export let apiUpdateFormTemplate = apiBaseLink + "/v1/form-templates" //PUT with /{id}
//Delete a form template with ID
export let apiDeleteFormTemplate = apiBaseLink + "/v1/form-templates" //DELETE with /{id}
//Get form template details with ID
export let apiGetFormTemplateDetails = apiBaseLink + "/v1/form-templates"  //GET with /{id}





