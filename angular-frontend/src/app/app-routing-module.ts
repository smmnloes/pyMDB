import {RouterModule, Routes} from "@angular/router";
import {SearchPageComponent} from "./components/content/search-page/search-page.component";
import {DetailsPageComponent} from "./components/content/details-page/details-page.component";
import {NgModule} from "@angular/core";
import {LoginComponent} from "./components/login/login.component";
import {RegisterComponent} from "./components/register/register.component";


const appRoutes: Routes = [
  {path: '', redirectTo: "/search", pathMatch: 'full'},
  {path: 'search', component: SearchPageComponent, runGuardsAndResolvers: 'paramsOrQueryParamsChange'},
  {path: 'details', component: DetailsPageComponent},
  {path: 'details/:movieId', component: DetailsPageComponent},
  {path: 'login', component: LoginComponent},
  {path: 'register', component: RegisterComponent},
  {path: '**', redirectTo:"/search"},
];


@NgModule({
  imports: [
    RouterModule.forRoot(appRoutes, {onSameUrlNavigation: 'reload', scrollPositionRestoration: 'enabled'})],
  exports: [RouterModule]
})

export class AppRoutingModule{}



