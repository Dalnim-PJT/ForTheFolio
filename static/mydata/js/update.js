// select2
$(document).ready(function() {
  $("#b_stack_multi").select2();
});	
$(document).ready(function() {
  $('[id^="p_stack_multi-"]').select2();
});
$(document).ready(function() {
  var typingTimer;
  var doneTypingInterval = 100;

  checkDuplicatetitle();

  $('#id_title').on('input', function() {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(checkDuplicatetitle, doneTypingInterval);
});

// 제목 중복 검사
  function checkDuplicatetitle() {
    var title = $('#id_title').val();
    var origin = $('#origin_title').val();

    if (!title) {
      $('#title-error').hide();
      $('#submit-button').prop('disabled', false);
      return;
    }
      $.ajax({
        url: '/portfolios/check/',
        type: 'GET',
        data: {'title': title, 'origin_title': origin},
        success: function(response) {
          if (response.duplicate) {
            $('#title-error').text('※ 중복된 title입니다.').show();
            $('#submit-button').prop('disabled', true); 
          } else {
            $('#title-error').hide();
            $('#submit-button').prop('disabled', false);
          }
        }
      });
  }
});

// 미리보기 창, input 인덱스 동일화
document.addEventListener("DOMContentLoaded", function() {
  const containerDivs = document.querySelectorAll(".image-preview-container");
  const inputElements = document.querySelectorAll('input[name^="pjt-"][name$="-image"]');
  const deleteElements = document.querySelectorAll('#delete-image');
  inputElements.forEach((inputElement, index) => {
    if (containerDivs[index]) {
      const containerIndex = containerDivs[index].id.split("-")[3];
      const inputIndex = inputElement.id.split("-")[2];
      
      if (containerIndex !== inputIndex) {
        inputElement.id = `image-upload-${containerIndex}`;
        inputElement.addEventListener("change", function (event) {
          handleImageUpload(event, containerIndex);
        });          
      }
    }
  });

// 등록된 이미지 미리보기 생성
  deleteElements.forEach((deleteElement, index) => {
    if (deleteElement) {
      const liElements = deleteElement.querySelectorAll("li");
      
      liElements.forEach(li => {
        const imageSrc = li.textContent.trim();
        if (imageSrc) {
          const imagePreview = document.createElement("div");
          imagePreview.className = "image-preview";
          const thumbnailImage = document.createElement("img");
          thumbnailImage.src = imageSrc;
          imagePreview.appendChild(thumbnailImage);
      
          const removeButton = document.createElement("div");
          removeButton.className = "remove-image-btn";
          removeButton.textContent = "x";
          removeButton.addEventListener("click", function () {
            li.querySelector('input').checked = true;
            imagePreview.remove();
            togglePlaceholderText(Number(index));
            event.stopPropagation();
          });
          
          imagePreview.appendChild(removeButton);
          containerDivs[index].appendChild(imagePreview);
          togglePlaceholderText(Number(index));
        }
      })
    }
  });
});

// 링크 창 추가
function addLinkField() {
  const linkEntries = document.getElementById("link-entries");
  const firstLinkEntry = linkEntries.firstElementChild;

  const newLinkEntry = document.createElement("div");
  newLinkEntry.className = "link-entry";
  const newIndex = linkEntries.childElementCount;
  newLinkEntry.innerHTML = firstLinkEntry.innerHTML.replace(/link-\d+/g, `link-0${newIndex}`);
  const formInputs = newLinkEntry.getElementsByTagName("input");
  for (let i = 0; i < formInputs.length; i++) {
    formInputs[i].value = "";
  }

  const existingCloseButton = newLinkEntry.querySelector("button");
  if (existingCloseButton) {existingCloseButton.remove()};
    
  const closeButton = document.createElement("button");
  closeButton.innerHTML = "&#10006;";
  newLinkEntry.appendChild(closeButton);

  linkEntries.appendChild(newLinkEntry);
}

document.getElementById("add-link-entry").addEventListener("click", addLinkField);
document.getElementById("link-entries").addEventListener("click", function(event) {
  if (event.target.tagName === "BUTTON") {
    event.preventDefault();
    const linkEntry = event.target.parentNode;

    if (document.getElementById("link-entries").childElementCount > 1) {
      linkEntry.remove();
    }
    else {        
      const formInputs = linkEntry.getElementsByTagName("input");
    for (let i = 0; i < formInputs.length; i++) {
      formInputs[i].value = "";
    }
  }
}
});

// 프로젝트 창 추가
function addPjtField() {
  const pjtEntries = document.getElementById("pjt-entries");
  const firstPjtEntry = pjtEntries.firstElementChild;

  const newPjtEntry = document.createElement("div");
  newPjtEntry.className = "pjt-entry";
  const newIndex = pjtEntries.childElementCount;
  newPjtEntry.innerHTML = firstPjtEntry.innerHTML.replace(/pjt-\d+/g, `pjt-0${newIndex}`);


  if (newPjtEntry.querySelector('#delete-image')) {
    newPjtEntry.querySelector('#delete-image').remove();
  }
  newPjtEntry.querySelector('.select').remove();
  newPjtEntry.querySelector('.select2').remove();

  const imageContainer = newPjtEntry.querySelector("#image-preview-container-0");
  const imageContents = imageContainer.querySelectorAll(".image-preview")
  
  imageContainer.setAttribute("id", `image-preview-container-${newIndex}`);
  imageContainer.setAttribute("name", `image-preview-container-${newIndex}`);
  imageContainer.setAttribute("ondrop", `handleImageDrop(event, ${newIndex})`);
  imageContainer.setAttribute("ondragover", "handleDragOver(event)");
  imageContainer.setAttribute("onclick", `openFileInput(${newIndex})`);
  imageContents.forEach((element) => {
    element.remove();
  });
  
  const placeholderText = newPjtEntry.querySelector("#placeholder-text-0");
  placeholderText.setAttribute("id", `placeholder-text-${newIndex}`);
  placeholderText.style.display = "block";

  const fileInput = newPjtEntry.querySelector("#image-upload-0");
  fileInput.setAttribute("id", `image-upload-${newIndex}`);
  fileInput.setAttribute("onclick", `openFileInput(${newIndex})`);
  fileInput.addEventListener("change", function (event) {
    handleImageUpload(event, newIndex);
  });

  const selectElement = document.createElement('select');
  selectElement.multiple = true;
  selectElement.setAttribute('class', 'select select2-hidden-accessible');
  selectElement.setAttribute('id', `p_stack_multi-${newIndex}`);
  selectElement.setAttribute('name', `p_stack_multi-${newIndex}`);
  selectElement.style.width = '335px';
  selectElement.style.height = '70px';
  selectElement.setAttribute("data-select2-id", `p_stack_multi-${newIndex}`);

  stacks.forEach((stack) => {
    const optionElement = document.createElement('option');
    optionElement.setAttribute('value', stack);
    optionElement.textContent = stack;
    selectElement.appendChild(optionElement);
  });

  const formInputs = newPjtEntry.getElementsByTagName("input");
  const formTexts = newPjtEntry.getElementsByTagName("textarea");
  for (let i = 0; i < formInputs.length; i++) {
    formInputs[i].value = "";
  }
  for (let i = 0; i < formTexts.length; i++) {
    formTexts[i].value = "";
  }

  const existingCloseButton2 = newPjtEntry.querySelector("button");
  if (existingCloseButton2) {existingCloseButton2.remove()};
    
  const closeButton = document.createElement("button");
  closeButton.innerHTML = "&#10006;";
  
  const pjtContentDiv = newPjtEntry.querySelector("#stack--box");

  pjtContentDiv.appendChild(selectElement);
  pjtContentDiv.appendChild(closeButton);

  newPjtEntry.appendChild(pjtContentDiv);
  pjtEntries.appendChild(newPjtEntry);
  

  $(`#p_stack_multi-${newIndex}`).select2();
}

document.getElementById("add-pjt-entry").addEventListener("click", addPjtField);
document.getElementById("pjt-entries").addEventListener("click", function(event) {
  if (event.target.tagName === "BUTTON") {
    event.preventDefault();
    const pjtEntry = event.target.closest(".pjt-entry");
    
    if (document.getElementById("pjt-entries").childElementCount > 1) {
      pjtEntry.remove();
    }
    // 필드 1개 남았을 때 전부 빈칸으로 셋팅
    else {        
      const formInputs = pjtEntry.getElementsByTagName('input[type="text"]');
      const formTexts = pjtEntry.getElementsByTagName("textarea");
      const formSelect = pjtEntry.querySelector("select");
      const selectOptions = formSelect.options;
      const selectBox = document.getElementById("stack--box");
      const selectViews = selectBox.querySelectorAll('li');
      const deleteImage =  pjtEntry.querySelector('#delete-image');
      const deleteImages =  deleteImage.querySelectorAll('input');
      
      if ( deleteImage ) {
        for (let i = 0; i < deleteImages.length; i++) {
          deleteImages[i].checked = true;
        }
        deleteImage.style.display = 'none';
      }
      for (let i = 0; i < selectOptions.length; i++) {
        selectOptions[i].selected = false;
      }
      for (let i = 0; i < selectViews.length; i++) {
        selectViews[i].remove();
      }
      for (let i = 0; i < formInputs.length; i++) {
        formInputs[i].value = "";
      }
      for (let i = 0; i < formTexts.length; i++) {
        formTexts[i].value = "";
      }
    }
  }

  // 필드 생략, 상세히
  if (event.target.closest("#more-btn")) {
    const moreBtn = event.target.closest("#more-btn");
    const entry = event.target.closest(".pjt-entry");
    const contentSections = entry.querySelectorAll(".pjt--content:not(:first-child)");
    const isReversed = moreBtn.classList.toggle('is-reversed');
    const isHidden = isReversed;

    for (let i = 0; i < contentSections.length; i++) {
      const section = contentSections[i];
      section.classList.toggle("pjt--content-hidden", isHidden);
    }
  }
});


// 드래그, 클릭 파일 리스트 생성
let uploadedFiles = {};

// 이미지 클릭 추가
function handleImageUpload(event, index) {
  const previewContainer = document.getElementById(`image-preview-container-${index}`);
  const files = event.target.files;

  if (!uploadedFiles[index]) {
  uploadedFiles[index] = [];
}

  for (const file of files) {
    if (!uploadedFiles[index].some(existingFile => existingFile.name === file.name)) {
      uploadedFiles[index].push(file);
    }

    addImageToPreview(previewContainer, file);
  }

  updateInputFiles(index);
  togglePlaceholderText(Number(previewContainer.getAttribute("id").split("-")[3]));
}

function handleDragOver(event) {
  event.preventDefault();
}

// 이미지 드래그 추가
function handleImageDrop(event, index) {
  event.preventDefault();
  const previewContainer = document.getElementById(`image-preview-container-${index}`);
  const files = event.dataTransfer.files;

  if (!uploadedFiles[index]) {
    uploadedFiles[index] = [];
  }

  for (const file of files) {
    if (!uploadedFiles[index].some(existingFile => existingFile.name === file.name)) {
      uploadedFiles[index].push(file);
    }
    addImageToPreview(previewContainer, file);
  }

  updateInputFiles(index);
  togglePlaceholderText(Number(previewContainer.getAttribute("id").split("-")[3]));
}

// 미리보기 생성
function addImageToPreview(previewContainer, file) {
  const reader = new FileReader();

  reader.onload = function (e) {
    const imagePreview = document.createElement("div");
    imagePreview.className = "image-preview";
    const image = new Image();
    image.src = e.target.result;
    image.alt = file.name;
    imagePreview.appendChild(image);

    const removeButton = document.createElement("div");
    removeButton.className = "remove-image-btn";
    removeButton.textContent = "x";
    removeButton.addEventListener("click", function () {
      imagePreview.remove();
      togglePlaceholderText(Number(previewContainer.getAttribute("id").split("-")[3]));
      event.stopPropagation();
    });
    
    imagePreview.appendChild(removeButton);
    previewContainer.appendChild(imagePreview);
    togglePlaceholderText(Number(previewContainer.getAttribute("id").split("-")[3]));
    
  };

  reader.readAsDataURL(file);
}

// 이미지 업로드 파일 리스트 생성

function updateInputFiles(index) {
  const inputElement = document.getElementById(`image-upload-${index}`);
  const dataTransfer = new DataTransfer();

  for (const file of uploadedFiles[index]) {
    dataTransfer.items.add(file);
  }

  inputElement.files = dataTransfer.files;
}

function openFileInput(index) {
  document.getElementById(`image-upload-${index}`).click();
}

// 이미지 첨부 텍스트 숨기기, 나타내기

function togglePlaceholderText(newIndex) {
  const placeholderText = document.getElementById(`placeholder-text-${newIndex}`);
  const previewContainer = document.getElementById(`image-preview-container-${newIndex}`);
  const previewContents = previewContainer.querySelector(".image-preview");
  if ( !previewContents ) {
    placeholderText.style.display = "block";
  } else {
    placeholderText.style.display = "none";
  }
}

document.getElementById(`image-upload-0`).addEventListener("change", function (event) {
  handleImageUpload(event, 0);
});

// 경력 필드 추가 
function addCareerField() {
  const careerEntries = document.getElementById("career-entries");
  const firstCareerEntry = careerEntries.firstElementChild;

  const newCareerEntry = document.createElement("div");
  newCareerEntry.className = "career-entry";
  const newIndex = careerEntries.childElementCount;
  newCareerEntry.innerHTML = firstCareerEntry.innerHTML.replace(/career-\d+/g, `career-0${newIndex}`);
  const formInputs = newCareerEntry.getElementsByTagName("input");
  for (let i = 0; i < formInputs.length; i++) {
    formInputs[i].value = "";
  }

  const existingCloseButton3 = newCareerEntry.querySelector("button");
  if (existingCloseButton3) {existingCloseButton3.remove()};
    
  const closeButton = document.createElement("button");
  closeButton.innerHTML = "&#10006;";
  newCareerEntry.appendChild(closeButton);

  careerEntries.appendChild(newCareerEntry);
}

document.getElementById("add-career-entry").addEventListener("click", addCareerField);
document.getElementById("career-entries").addEventListener("click", function(event) {
  if (event.target.tagName === "BUTTON") {
    event.preventDefault();
    const careerEntry = event.target.parentNode;
    
    
    if (document.getElementById("career-entries").childElementCount > 1) {
      careerEntry.remove();
    }
    else {        
      const formInputs = careerEntry.getElementsByTagName("input");
    for (let i = 0; i < formInputs.length; i++) {
      formInputs[i].value = "";
    }
  }
}
});

// 프로필 이미지 미리보기
function previewImage(event) {
  var input = event.target;
  var imageURL = input.dataset.imageUrl;
  if (input.files && input.files[0]) {
    var reader = new FileReader();
  
    reader.onload = function(e) {
      var preview = document.querySelector('#preview-image');
      preview.setAttribute('src', e.target.result);
      preview.style.display = 'block';
    };
  
    reader.readAsDataURL(input.files[0]);
  } else if (imageURL) {
    var preview = document.querySelector('#preview-image');
    preview.setAttribute('src', imageURL);
    preview.style.display = 'block';
  }
}

var imageInput = document.querySelector('#id_image');
imageInput.addEventListener('change', previewImage);

window.addEventListener('load', function () {
  var event = new Event('change', { bubbles: true });
  imageInput.dispatchEvent(event);
});