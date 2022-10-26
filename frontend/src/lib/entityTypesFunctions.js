// import { apiGetAllEntityTypes } from '$lib/stores'

// export async function getAllEntityTypes() {
//     //API CALL
//     console.log("API CALL: GET ALL ENTITY TYPES");

//     try {
//         const response = await fetch(apiGetAllEntityTypes)
//         const entityTypes = await response.json()
    
//         if (response.ok) {
//             let resultStr = JSON.stringify(entityTypes)
//             console.log(new Date().toUTCString() + " RETURNED ENTITY TYPES RESULT: " + resultStr);
//             return entityTypes;
//         } else {
//             console.log("ENTITY TYPES RESPONSE NOT OK")
//         }
//     } catch (error) {
//             console.log("ENTITY TYPES ERROR: " + error);
//     }
// }