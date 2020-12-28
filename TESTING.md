### Issues and Resolutions to issues found during development testing
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