/*
 * Copyright 2020 EraO Prosopagnosia Helper Dev Team, Liren Pan, Yixiao Hong, Hongzheng Xu, Stephen Huang, Tiancong Wang
 *
 * Supervised by Prof. Steve Mann (http://www.eecg.toronto.edu/~mann/)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

// function init(){
//     console.log("inited");
//     var form = document.getElementById("register");
//         form.addEventListener("submit", event =>{
//         event.preventDefault();
//         var noErr = true;
//         // get all the inputs within the submitted form
//         var inputs = form.getElementsByClassName('field');
//         for (var i = 0; i < inputs.length; i++) {
//             // only validate the inputs that have the required attribute
//             if(inputs[i].value === ""){
//                 // found an empty field that is required
//                 alert("Please fill all required fields");
//                 noErr = false;
//             }
//         }
//         if (noErr) {
//             form.submit();
//         }
//     }, false);
// }
// //window.addEventListener("load", init, false);