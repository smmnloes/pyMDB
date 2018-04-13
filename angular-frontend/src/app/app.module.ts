import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {FormsModule} from "@angular/forms";
import {HttpClientModule} from "@angular/common/http";

import {AppComponent} from './app.component';
import {HeaderComponent} from './header/header.component';
import {ContentComponent} from './content/content.component';
import {SearchPageComponent} from './content/search-page/search-page.component';
import {SearchFormComponent} from './content/search-page/search-form/search-form.component';
import {SearchResultsComponent} from './content/search-page/search-results/search-results.component';
import {AngularMultiSelectModule} from "angular2-multiselect-dropdown/angular2-multiselect-dropdown";
import {MultiselectComponent} from './content/search-page/search-form/multiselect/multiselect.component';
import {QueryService} from "./query.service";
import {ResultComponent} from './content/search-page/search-results/result/result.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    ContentComponent,
    SearchPageComponent,
    SearchFormComponent,
    SearchResultsComponent,
    MultiselectComponent,
    ResultComponent
  ],
  imports: [
    BrowserModule,
    AngularMultiSelectModule,
    FormsModule,
    HttpClientModule
  ],
  providers: [QueryService],
  bootstrap: [AppComponent]
})
export class AppModule { }
