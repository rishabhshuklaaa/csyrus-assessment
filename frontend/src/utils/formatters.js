/**
 * Formats dirty ISO date strings into readable layout strings.
 */
export const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

/**
 * Maps categorical priority statuses directly to TailwindCSS aesthetic design system badges.
 */
export const getPriorityStyles = (priority) => {
  const normalized = priority?.toUpperCase() || 'LOW';
  switch (normalized) {
    case 'HIGH':
      return 'bg-red-100 text-red-800 border border-red-200 px-2 py-1 rounded-full text-xs font-semibold';
    case 'MEDIUM':
      return 'bg-yellow-100 text-yellow-800 border border-yellow-200 px-2 py-1 rounded-full text-xs font-semibold';
    default:
      return 'bg-green-100 text-green-800 border border-green-200 px-2 py-1 rounded-full text-xs font-semibold';
  }
};