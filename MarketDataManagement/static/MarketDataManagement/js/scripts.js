/**
 * 
 */

function overlayClick(overlayID) {
	el = document.getElementById(overlayID);
	el.style.visibility = (el.style.visibility == "visible") ? "hidden" : "visible";
}
