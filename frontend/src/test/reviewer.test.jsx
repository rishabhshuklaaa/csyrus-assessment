import React from 'react';
import { describe, test, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import RequestCard from '../components/RequestCard.jsx';


vi.mock('../utilis/formatters', () => ({
  getPriorityStyles: vi.fn(() => 'mock-badge-class'),
  formatDate: vi.fn(() => 'Jan 01, 2026')
}));

describe('Reviewer Decision Matrix and State Transitions', () => {
  const mockRequestItem = {
    id: 'req-abc-123',
    title: 'Enterprise Server Allocation',
    description: 'Upgrading cluster computational limits.',
    priority: 'HIGH',
    status: 'PENDING',
    reviewer_id: 'rev-uuid-string-format'
  };

  test('RequestCard must render distinct priority badge styling definitions cleanly', () => {
    const mockEdit = vi.fn();
    const mockDelete = vi.fn();

    render(
      <RequestCard 
        request={mockRequestItem} 
        onEdit={mockEdit} 
        onDelete={mockDelete} 
      />
    );

    expect(screen.getByText('Enterprise Server Allocation')).toBeInTheDocument();
    expect(screen.getByText('HIGH')).toBeInTheDocument();
    expect(screen.getByText('PENDING')).toBeInTheDocument();
  });

  test('Action operation controls must unlock execution loops on click', () => {
    const mockEdit = vi.fn();
    const mockDelete = vi.fn();

    render(
      <RequestCard 
        request={mockRequestItem} 
        onEdit={mockEdit} 
        onDelete={mockDelete} 
      />
    );

    const editButton = screen.getByText('Edit');
    fireEvent.click(editButton);

    expect(mockEdit).toHaveBeenCalledWith(mockRequestItem);
  });
});
