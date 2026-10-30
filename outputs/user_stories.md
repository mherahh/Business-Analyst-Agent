# Agile User Stories & Acceptance Criteria: Campus Connect

## US-01 [Must]: User Registration and Login

- **User Story**: As a New user, I want to register and log in to the application, so that I can access my account and manage my events.
- **Linked Requirements**: FR-01
- **Acceptance Criteria (Gherkin BDD)**:
- - **AC-01 (Successful user registration)**: Given I am on the registration page, When I enter valid registration details and submit the form, Then I should receive a confirmation email and be redirected to the login page.
- - **AC-02 (Successful user login)**: Given I have a registered account, When I enter my valid credentials and click the login button, Then I should be logged in and redirected to my account dashboard.
- - **AC-03 (Failed user login with invalid credentials)**: Given I am on the login page, When I enter invalid credentials and click the login button, Then I should see an error message indicating invalid credentials.

## US-02 [Must]: Browse and Search Events

- **User Story**: As a User, I want to browse and search for events based on various criteria, so that I can find events that interest me.
- **Linked Requirements**: FR-02
- **Acceptance Criteria (Gherkin BDD)**:
- - **AC-04 (Browse events without filters)**: Given I am on the events page, When I do not apply any filters and click the browse button, Then I should see a list of all available events.
- - **AC-05 (Search events by keyword)**: Given I am on the events page, When I enter a keyword in the search bar and click search, Then I should see a list of events that match the keyword.
- - **AC-06 (Filter events by date)**: Given I am on the events page, When I select a date range and click apply filters, Then I should see a list of events occurring within the selected date range.

## US-03 [Must]: Event Registration

- **User Story**: As a User, I want to register for events, so that I can participate in the events I am interested in.
- **Linked Requirements**: FR-07
- **Acceptance Criteria (Gherkin BDD)**:
- - **AC-07 (Successful event registration)**: Given I am logged in and viewing an event, When I click the register button for the event, Then I should receive a confirmation message and see the event in my registered events list.
- - **AC-08 (Failed event registration due to full capacity)**: Given I am logged in and viewing a fully booked event, When I click the register button for the event, Then I should see a message indicating that the event is fully booked.

## US-04 [Should]: Create and Manage Events

- **User Story**: As a Event organizer, I want to create and manage my events, so that I can keep track of my events and make updates as needed.
- **Linked Requirements**: FR-03
- **Acceptance Criteria (Gherkin BDD)**:
- - **AC-09 (Create a new event)**: Given I am logged in as an event organizer, When I fill in the event details and click the create event button, Then The event should be created and appear in my events list.
- - **AC-10 (Edit an existing event)**: Given I am logged in as an event organizer and have an existing event, When I update the event details and click the save button, Then The event should be updated with the new details.

## US-05 [Should]: Admin Dashboard

- **User Story**: As a Admin user, I want to access an admin dashboard, so that I can manage events and users effectively.
- **Linked Requirements**: FR-04
- **Acceptance Criteria (Gherkin BDD)**:
- - **AC-11 (Access admin dashboard)**: Given I am logged in as an admin user, When I navigate to the admin dashboard, Then I should see the admin dashboard with options to manage events and users.
- - **AC-12 (Manage user accounts from admin dashboard)**: Given I am on the admin dashboard, When I select a user account to manage, Then I should be able to view and edit the user's details.

## US-06 [Could]: Email Notifications

- **User Story**: As a User, I want to receive email notifications for event reminders and updates, so that I can stay informed about the events I am interested in.
- **Linked Requirements**: FR-05
- **Acceptance Criteria (Gherkin BDD)**:
- - **AC-13 (Receive email notifications for event updates)**: Given I am registered for an event and have opted in for notifications, When The event details are updated, Then I should receive an email notification about the updates.

## US-07 [Could]: Event Recommendations

- **User Story**: As a User, I want to receive recommendations for events based on my preferences, so that I can discover new events that I might enjoy.
- **Linked Requirements**: FR-06
- **Acceptance Criteria (Gherkin BDD)**:
- - **AC-14 (Receive event recommendations)**: Given I am logged in and have attended events in the past, When I visit the recommendations page, Then I should see a list of recommended events based on my preferences.
