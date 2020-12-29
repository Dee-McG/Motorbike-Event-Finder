# Test Results

## User Story Testing

### User Story:
> As a user, I want the main purpose of the site to be clear so that I immediately know what the site is intended for upon entering.

Tests Covering story:
* TC021

### User Story:
> As a user, I want to easily navigate the site so that I can find content quickly with ease.

Tests Covering story:
* TC008
* TC009
* TC010

### User Story:
> As a user, I want the website to be responsive so that I can clearly view the webpages from my mobile, tablet or desktop.

Tests Covering story:
* TC005
* TC006
* TC007

### User Story:
> As a user, I want to be able to register to the website so that I can create and manage my own events.

Tests Covering story:
* TC014
* TC015
* TC016
* TC017
* TC018

### User Story:
> As a user, I want to be able to search or filter events based on custom criteria so that I can find events suited to me.

Tests Covering story:
* TC012

### User Story:
> As a user, I want a way to contact the site owner so that I can have any questions I may have in regards to the website answered.

Tests Covering story:
* TC013

### User Story:
> As a user, I want to be able to return to the main site without having to use the browser buttons so that I can easily return to the website if I navigate to a page that doesn't exist.

Tests Covering story:
* TC019

***
## Issues and Resolutions to issues found during testing of deployed website

Issue #1: 
> TC001 - Step 3: Failed validation on type="text" being invalid attribute on select element.

FIX - This was resolved by removing the type="text" attribute.

Issue #2:
> TC001 - Step 4: Failed validation with warning on script tags not needing type attributes.

FIX - This was fixed by removing the type attribute.

Issue #3:
> TC014 - Step 3: Forms did not alert user of correct inputs into the Sign Up form.

FIX - This was resolved by adding custom error messages directly on the form fields.

Issue #4:
> TC017 - Step 3: Users "Name" is not displaying on profile when collection field is not blank.

FIX - This issue was resolved by removing the return field ["username"] and updating the profile code to search for correct values.

***
## Issues and Resolutions to issues found during development testing
Issue #1: 
> On small devices on the Sign Up form, the label text was over lapping the text input 

This was resolved by 
removing the (Optional) text from the label and adding it as placeholder text.

Issue #2:
> Form labels missing. During a lighthouse report generation, it was found that many form elements across the 
website were missing labels. 

This was fixed by adding labels to the form elements.

Issue #3:
> Anchor link on home page main content section was redirecting to the Events page. 

This was fixed by correcting the url_for to 'signup'.

Issue #4:
> Event type wasn't populating the drop down list on the events page.

This was resolved by correcting the url_for link and passing caregories list to the template.

Issue #5:
> When sorting events by date (string) from MongoDB collection, they were sorting on the days instead of full dates.

This was resolved by parsing the dates into datetime objects and then sorting them.