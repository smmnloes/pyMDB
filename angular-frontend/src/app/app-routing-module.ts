import {RouterModule, Routes} from "@angular/router";
import {SearchPageComponent} from "./header/content/search-page/search-page.component";
import {DetailsPageComponent} from "./header/content/details-page/details-page.component";
import {NgModule} from "@angular/core";


const appRoutes: Routes = [
  {path: '', redirectTo: "/search", pathMatch: 'full'},
  {path: 'search', component: SearchPageComponent, runGuardsAndResolvers: 'paramsOrQueryParamsChange'},
  {path: 'details', component: DetailsPageComponent},
  {path: 'details/:movieId', component: DetailsPageComponent},
];


@NgModule({
  imports: [
    RouterModule.forRoot(appRoutes, {onSameUrlNavigation: 'reload'})],
  exports: [RouterModule]
})

export class AppRoutingModule{}



