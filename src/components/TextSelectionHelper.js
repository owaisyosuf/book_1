/**
 * Text Selection Helper for the RAG Chatbot
 * Provides functionality to get selected text and context
 */

export const getTextSelectionContext = () => {
  const selection = window.getSelection();
  if (!selection.toString().trim()) {
    return null;
  }

  const range = selection.getRangeAt(0);
  const selectedText = selection.toString().trim();

  // Get the surrounding context of the selection
  const contextRange = range.cloneRange();
  const maxLength = 500; // Maximum context length

  // Expand the range to capture more context
  contextRange.expand('word');

  // Try to get more context by extending the range
  try {
    // Move the start boundary backward to get more context
    contextRange.setStart(range.startContainer, Math.max(0, range.startOffset - 50));
    // Move the end boundary forward to get more context
    contextRange.setEnd(range.endContainer, Math.min(
      range.endContainer.length || range.endContainer.textContent.length,
      range.endOffset + 50
    ));

    // Limit the context length
    let contextText = contextRange.toString().substring(0, maxLength);

    return {
      selectedText,
      contextText,
      fullRange: range
    };
  } catch (e) {
    // If we can't expand the range, just return the selected text
    return {
      selectedText,
      contextText: selectedText,
      fullRange: range
    };
  }
};

// Function to highlight selected text temporarily
export const highlightSelection = () => {
  const selection = window.getSelection();
  if (selection.rangeCount > 0) {
    const range = selection.getRangeAt(0);
    const span = document.createElement('span');
    span.style.backgroundColor = 'yellow';
    span.style.opacity = '0.3';
    range.surroundContents(span);

    // Remove the highlight after a short time
    setTimeout(() => {
      if (span.parentNode) {
        const content = document.createTextNode(span.textContent);
        span.parentNode.replaceChild(content, span);
      }
    }, 1000);
  }
};

// Function to get the chapter/section information where the selection occurred
export const getSelectionLocation = () => {
  const selection = window.getSelection();
  if (selection.rangeCount === 0) return null;

  const range = selection.getRangeAt(0);
  const element = range.commonAncestorContainer;

  // Try to find the closest article or section element to determine context
  let sectionElement = element.closest('article, section, .markdown');
  if (!sectionElement) {
    sectionElement = element.parentElement;
  }

  // Try to get the heading associated with this content
  let heading = null;
  if (sectionElement) {
    // Look for the closest heading above the selected content
    let prevElement = sectionElement.previousElementSibling;
    while (prevElement) {
      if (prevElement.tagName.match(/^H[1-6]$/)) {
        heading = prevElement.textContent;
        break;
      }
      prevElement = prevElement.previousElementSibling;
    }
  }

  return {
    heading: heading || 'Unknown Section',
    element: sectionElement ? sectionElement.tagName.toLowerCase() : 'unknown'
  };
};