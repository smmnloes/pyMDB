import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-credits',
  templateUrl: './credits.component.html',
  styleUrls: ['./credits.component.css']
})
export class CreditsComponent implements OnInit {
  @Input()
  credits:string[][];

  constructor() { }

  ngOnInit() {
  }

}
