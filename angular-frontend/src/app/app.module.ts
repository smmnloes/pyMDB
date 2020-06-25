import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {FormsModule} from "@angular/forms";
import {HttpClientModule} from "@angular/common/http";

import {AppComponent} from './app.component';
import {HeaderComponent} from './components/header/header.component';
import {SearchPageComponent} from './components/content/search-page/search-page.component';
import {SearchFormComponent} from './components/content/search-page/search-form/search-form.component';
import {SearchResultsComponent} from './components/content/search-page/search-results/search-results.component';
import {QueryService} from "./services/query.service";
import {ResultComponent} from './components/content/search-page/search-results/result/result.component';
import {PaginationComponent} from './components/content/search-page/search-results/pagination/pagination.component';
import {DetailService} from "./services/detail.service";
import {DetailsPageComponent} from './components/content/details-page/details-page.component';
import {CreditsComponent} from './components/content/details-page/credits/credits.component';
import {AppRoutingModule} from "./app-routing-module"
import {FooterComponent} from './components/footer/footer.component';
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {ToastrModule} from "ngx-toastr";
import {MultiSelectAllModule} from "@syncfusion/ej2-angular-dropdowns";
import {LoginComponent} from './components/login/login.component';
import {RegisterComponent} from './components/register/register.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    SearchPageComponent,
    SearchFormComponent,
    SearchResultsComponent,
    ResultComponent,
    PaginationComponent,
    DetailsPageComponent,
    CreditsComponent,
    FooterComponent,
    LoginComponent,
    RegisterComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    MultiSelectAllModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    ToastrModule.forRoot({positionClass: 'toast-top-center', timeOut: 3000})
  ],
  providers: [QueryService, DetailService],
  bootstrap: [AppComponent]
})
export class AppModule {
}
